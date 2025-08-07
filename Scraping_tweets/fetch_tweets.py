import tweepy
from pymongo import MongoClient
import json
import time
from config import TWITTER_API_KEYS

# Configuration de l'API Twitter v2
client = tweepy.Client(bearer_token=TWITTER_API_KEYS['BEARER_TOKEN'])

# Connexion à MongoDB
mongo_client = MongoClient('localhost', 27017)
db = mongo_client['db']
collection = db['tweets_inwi']

output_file = 'tweets.json'


# Fonction pour récupérer TOUS les commentaires d'un tweet
def fetch_comments(tweet_id, retries=3):
    comments = []
    next_token = None
    attempts = 0

    while attempts < retries:
        try:
            while True:

                replies = client.search_recent_tweets(
                    query=f"conversation_id:{tweet_id}",
                    max_results=10,
                    tweet_fields=['created_at', 'public_metrics'],
                    next_token=next_token
                )

                if replies.data:
                    for reply in replies.data:
                        comments.append({
                            'comment_order': len(comments) + 1,
                            'comment_date': str(reply.created_at),
                            'comment_text': reply.text,
                            'comment_likes': reply.public_metrics['like_count']
                        })
                    print(f"{len(comments)} commentaire(s) récupéré(s) pour {tweet_id}")

                next_token = replies.meta.get('next_token')
                if not next_token:
                    break

                time.sleep(3)

            return comments

        except (tweepy.TooManyRequests, tweepy.TweepyException, ConnectionError) as e:
            print(f"Erreur lors de la récupération des commentaires pour {tweet_id} : {e}")
            attempts += 1
            if attempts < retries:
                print(f"Nouvelle tentative dans 10 secondes... ({attempts}/{retries})")
                time.sleep(10)
            else:
                print("Échec après plusieurs tentatives. Commentaire par défaut ajouté.")

    # Ajouter un commentaire par défaut en cas d'erreur
    if not comments:
        comments.append({
            'comment_order': 0,
            'comment_date': None,
            'comment_text': "No comments available",
            'comment_likes': 0
        })

    return comments


# Fonction pour sauvegarder chaque tweet dans JSON
def save_to_json(tweet_data):
    try:
        tweet_data['_id'] = str(tweet_data.get('_id', ''))
        with open(output_file, 'a', encoding='utf-8') as f:
            json.dump(tweet_data, f, ensure_ascii=False, indent=4)
            f.write(",\n")
        print("Tweet sauvegardé dans JSON.")
    except Exception as e:
        print(f"Erreur de sauvegarde JSON : {e}")

# Fonction pour récupérer les tweets et leurs commentaires
def fetch_tweets(query, total_tweets=50):
    fetched_tweets = 0

    while fetched_tweets < total_tweets:
        try:
            remaining_tweets = min(10, total_tweets - fetched_tweets)


            tweets = client.search_recent_tweets(
                query=query,
                max_results=remaining_tweets,
                tweet_fields=['created_at', 'public_metrics', 'conversation_id', 'author_id']
            )
            if tweets.data:
                for tweet in tweets.data:
                    print(f"🔹 Tweet récupéré : {tweet.text[:50]}...")

                    comments = fetch_comments(tweet.id)

                    # Structuration des données du tweet
                    data = {
                        'tweet_id': tweet.id,
                        'tweet_date': str(tweet.created_at),
                        'nbr_likes': tweet.public_metrics['like_count'],
                        'nbr_retweets': tweet.public_metrics['retweet_count'],
                        'nbr_caracters': len(tweet.text),
                        'author_id': tweet.author_id,
                        'text': tweet.text,
                        'comments': comments
                    }

                    result = collection.insert_one(data)
                    data['_id'] = result.inserted_id
                    save_to_json(data)
                    print(f"Tweet inséré avec {len(comments)} commentaire(s)")
                    time.sleep(5)  
                fetched_tweets += len(tweets.data)

        except tweepy.TooManyRequests:
            print("Erreur 429 - Pause de 5 minutes...")
            time.sleep(300)
        except Exception as e:
            print(f"Erreur générale : {e}")


# Exécution principale pour récupérer 50 tweets sur Inwi et 50 sur télécoms marocains
if __name__ == "__main__":
    queries = [
        ("forfait inwi ", 50),  # 50 tweets sur Inwi
        ("télécom Maroc OR Maroc Telco", 50)  # 50 tweets sur le secteur télécom
    ]

    while True:
        for query, total in queries:
            print(f"🔍 Recherche de {total} tweets pour '{query}'...")
            fetch_tweets(query, total)
            print(f" Terminé pour '{query}'. Pause de 1 minute avant la prochaine recherche...")
            time.sleep(60)  # Pause de 1 minute entre les recherches

        print("Reprise du cycle pour s'assurer qu'aucun tweet n'a été manqué.")