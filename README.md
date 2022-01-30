# Les Projets


Cette année pour l'évaluation, vous serez assez libre.

## Consignes

- Vous devez créer une application Web vous basant sur le package Flask.
- Votre application devra récupérer des données sur le web soit des données Open Data soit des données scrapées grâce à ce que vous aurez appris durant ce cours.
- Votre application devra afficher les données de façon optimale, moteur de recherche, graphiques, etc. 
- Vous devrez utiliser une ou plusieurs bases de données abordées dans ce cours. 
- Vous devrez créer une documentation technique et fonctionnelle.  

## Evaluation

- [] Bonus scraping  

- [] Bonus scraping temps réel  

- [] Bonus Docker 

- [] Bonus Docker-compose  



# RAPPORT DE NOTRE PROJET

Notre plateforme se base sur certaines données de la Formule 1, d'où nous avons extrait les informations concernant les informations et statistiques de courses allant des années 2012 à 2021. Nous allons pour cela 
exploiter deux sites web:

  - Le premier site est [`Formula 1`](https://www.formula1.com/), avec comme page de départ le site officiel d'information de la Formule 1, avec comme page de départ, [`la saison 2021`](https://www.formula1.com/en/results.html/2021/races.html)
      
  - Le deuxième site étant [`f1fca`](https://www.f1cfa.com/f1-tyres-statistics.asp?t=2021&gpn=All&tipo=All&driver=All), un site nous donnant chaque set de pneus utilisé lors de chaque Grand Prix.


# INSTALLATION ET UTILISATION DES FICHIERS

## Installation de Git et récupération des fichiers
\
Vérifiez tout d'abord que vous avez installé [Git](https://git-scm.com/) pour la récupération des fichiers.

Nous allons maintenant cloner le projet dans le répertoire de votre choix. Pour cela, cliquez sur votre répertoire et faites clique-droit `Git Bash Here`.

Une fois Git Bash ouvert, nous allons cloner le répertoire en ligne où se trouve le projet. Cliquez sur le bouton `Clone or Download` et copiez l'adresse HTTPS du [répertoire](https://git.esiee.fr/duongh/data-engineering-1.git).

Une fois copié, retournez dans Git Bash et tapez la commande `git clone` (adresse du répertoire) et cela vous donnera un accès de téléchargement au répertoire.
Finalement, tapez la commande `git pull` et vous aurez à votre disposition tous les fichiers du projet. 


## Comprendre les fichiers
\
Une fois la source de notre projet extraite, allez dans le dossier `Projet` et là se trouveront plusieurs fichiers dont les plus essentiels sont les suivants:

- Le fichier [`main.py`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/main.py) qui est le coeur de notre plateforme, permettant à la fois la gestion des données, à savoir le scrapping et le traitement des données, mais également la redirection vers les pages correspondantes aux appels d'actions de l'utilisateur.
- Le dossier [`File_crawler`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/tree/master/Data_Projet) contenant les fichiers [`spiders`](https://www.kaggle.com/mylesoneill/world-university-rankings?=select=timesData.csv), fichiers prenant les informations sur les pages en ligne.
- Le fichier [`requirement.txt`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/requirements.txt) contenant tous les packages nécessaires au bon fonctionnement de notre plateforme.
- Le fichier [`data_scrap.py`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/get_data.py) permettant de lancer le crawling des informations des deux sites webs
- Le fichier [`insert_db.py`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/blob/master/kaggle.json), permettant de faire le tri de données et l'insertion dans la base de données MongoDB à l'aide des fichiers jsons qui ont été crawlés.
- Le dossier [`templates`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/tree/master/assets) concernant les différentes pages de notre plateforme.
- Le dossier [`static`](https://git.esiee.fr/duongh/python-pour-la-data-science/-/tree/master/assets) concernant les différentes images et fonctionnalités de structure de notre plateforme.

Tous ces composants vont pouvoir être lancer à l'aide d'un seul fichier, le `dockerfile`. La structure entière tournera donc autour de deux fichiers principaux:
- Le `dockerfile`, permettant de créer notre volume (environnement de travail) qui permettra de tout centraliser.
- Et un `docker-compose.yml` appelant les différentes technologies que nous utilisons, ici `mongo` en base de données et notre fichier `main.py` comme fichier de compilation central.


# USER'S GUIDE 

## Installation des packages nécessaires
\
Vérifiez tout d'abord si vous disposez de la bonne version de Python. Pour cela:
- ouvrir l'invite de commandes de Windows (Windows+R, puis tapez cmd)
- dans l'invite de commandes tapez `python --version`
- vérifiez si la version est à jour, de préférence la version `3.9.7`

Certains packages seront également nécessaires à installer pour la bonne utilisation du dash si cela n'est pas déjà fait :
- ouvrir l'invite de commandes et se rendre dans le dossier du projet
- tapez la commande `docker compose up`, cette commande va permettre de concevoir les containers nécessaires à la plateforme.

Une fois la commande tapée pour démarrer le fichier principal `main.py`, une addresse locale va s'ouvrir dans le terminal, il ne reste plus qu"à se rendre sur cette adresse pour accéder à la plateforme. 


## Fonctionnement de l'application Web
\
Une fois le fichier lancé, le terminal va fournir une adresse url local, ici `http://127.0.0.1:2747/`. Tapez cette adresse va nous renvoyer vers notre navigateur par défaut (de préférence Chrome ou Brave) et charger la page. 

Une fois la page chargée, cela va directement vous renvoyer vers la page d'accueil de la plateforme.
Vous pourrez apercevoir 3 choix possibles de navigation: 
  - les `Drivers`, pilotes ayant concurrus en Formule 1
  - les `Teams`, constructeurs et écuries de la Formule 1
  - les `Grand Prix`, information des Grands Prix des années passées

\
\
Le premier bouton va vous renvoyer la liste de tous les pilotes ayant courus en Formule de 2012 à 2021. A vous de choisir les informations qui vous intéressent :) .

Une fois le pilote choisi, il y aura comme informations générales un graphe principal donnant en information de courbe les points du pilote en fonction de l'année, ainsi que son positionnement dans le championnat cet année-là.

On pourra également y retrouvé dans des formats tableaux des informations complémentaires du pilote, notamment son nombre de victoire et de pôle position (s'il en a eu), son nombre d'abandon, ses meilleures positions moyennes dans chaque Grand Prix, et ses récentes participations aux Grand Prix. 
\
\
Le deuxième bouton de la page d'accueil va vous renvoyer la liste de tous les constructeurs qu'il y a eu entre les 2012 et 2021, avec comme précision le nom du moteur utilisé en fin de nom.

Sur cette page nous allons retrouver les points du constructeur chaque année qu'il a participée en graphique, la position moyenne du championnat par année sur les Grand Prix, les meilleurs temps d'arret (Pit Stops) de l'écurie et le nombre d'abandons total de chacun de leur pilote dans leur temps avec le constructeur.


# DEVELOPPER'S GUIDE

## Structure de l'architecture
\
Après avoir énumérer les étapes et fichiers nécessaires à l'initialisation de notre plateforme, voyons maintenant la structure de notre dossier projet:
- Dockerfile
- docker-compose.yml
- main.py
- insert_db.py
- data_scrap.py
- scrapy.cfg (le fichier permettant le scrapping dans ce dossier)
- File_crawler/
  + Spiders/ (les fichiers qui vous crawler nos pages de données)
  + items.py
  + middleware.py
  + pipelines.py
  + settings.py
- static/
  + styles/ (notre fichier css pour la personnalisation de nos pages html)
  + images (en PNG)
- templates/
  + nos pages html

\
Dans la partie `main` de notre projet `main.py`, on peut voir deux fonctions appelées au préalable : `scrap()` et `insert_db()`, ces deux fonctions venant des fichiers de `data_scrap.py` pour le scrapping de nos pages et `insert_db.py` pour l'insertion des données dans la base de données MongoDB pour le traitement des informations.
\
Nous allons donc ici utiliser deux technologies: `Scrappy` et `Mongo`, le tout visualisé sur une application `Flask`.
\
## First Step: Extraction des données
\
Analysons le fichier `data_scrap.py`. Le début du fichier va tout d'abord les fichiers apparents à la plateforme pour renouveler les données en temps réel en gérant les exceptions des fichiers.
Puis ce fichier va éxécuter des commandes de `scrapy crawl` des fichiers spiders présents dans le dossier `File_crawler`. 







