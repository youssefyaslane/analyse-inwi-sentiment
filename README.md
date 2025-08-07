# 📊 Analyse de Sentiment des Tweets Inwi

## 🔍 Objectif
Ce projet a pour but de **collecter, stocker et analyser les sentiments exprimés dans les tweets** mentionnant l'opérateur télécom marocain **Inwi**, afin d’identifier les perceptions positives et négatives de ses utilisateurs.

---

## 🧱 Structure du Projet

```
.
├── Analyse_tweets/
│   ├── analyse_sentiment.ipynb           # Analyse tweets
│   ├── analyse_sentiment_bert.ipynb      # Analyse basée sur BERT
│
├── data/
│   ├── tweets.csv                        # Tweets formatés
│   ├── negative_tweets.csv               # Tweets négatifs
│   ├── tweeet.png                       
│   └── tweets.json                       # Données brutes en JSON
│
├── Scraping_tweets/
│   ├── config.py                         # Clé API Twitter
│   ├── fetch_tweets.py                   # Script de récupération des tweets
│   └── tweets.json                       # JSON de sauvegarde
│
├── doc/                                  # (Optionnel) Documentation
└── README.md                             # Fichier descriptif du projet
```

---

## ⚙️ Fonctionnalités principales

1. **Collecte des tweets**
   - Utilisation de l’API Twitter (via `tweepy`) pour rechercher les tweets mentionnant "Inwi" ou les télécoms marocains.
   - Sauvegarde des tweets dans MongoDB + export en JSON.

2. **Nettoyage et traitement**
   - Suppression des doublons, liens, emojis, mentions inutiles, etc.
   - Analyse lexicale pour préparer les données au traitement du langage.

3. **Analyse de sentiment**
     - `BERT` (modèle pré-entraîné) pour une analyse fine des émotions.

4. **Visualisation**
   - Graphiques des tweets positifs/négatifs/neutres.
   - Nuage de mots.
   - Illustration par capture d’écran.

---

## 🛠️ Installation et Lancement

1. Cloner le repo :
```bash
git clone https://github.com/ton-utilisateur/nom-du-repo.git
cd nom-du-repo
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Ajouter les clés API dans `config.py` :
```python
TWITTER_API_KEYS = {
    'BEARER_TOKEN': 'VOTRE_CLE_IÇI'
}
```

4. Lancer la collecte :
```bash
python fetch_tweets.py
```

5. Exécuter les notebooks pour l’analyse (`.ipynb`)

---

## 🧑‍💻 Auteur

**Youssef Yaslane** — *Data Scientist | Big Data & IA Engineer*