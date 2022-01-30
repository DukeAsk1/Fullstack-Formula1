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

- Le fichier [`main.py`](https://git.esiee.fr/duongh/data-engineering-1/-/blob/master/Projet/main.py) qui est le coeur de notre plateforme, permettant à la fois la gestion des données, à savoir le scrapping et le traitement des données, mais également la redirection vers les pages correspondantes aux appels d'actions de l'utilisateur.
- Le dossier [`File_crawler`](https://git.esiee.fr/duongh/data-engineering-1/-/tree/master/Projet/File_crawler) contenant les fichiers [`spiders`](https://www.kaggle.com/mylesoneill/world-university-rankings?=select=timesData.csv), fichiers prenant les informations sur les pages en ligne.
- Le fichier [`requirement.txt`](https://git.esiee.fr/duongh/data-engineering-1/-/blob/master/Projet/requirements.txt) contenant tous les packages nécessaires au bon fonctionnement de notre plateforme.
- Le fichier [`data_scrap.py`](https://git.esiee.fr/duongh/data-engineering-1/-/blob/master/Projet/data_scrap.py) permettant de lancer le crawling des informations des deux sites webs
- Le fichier [`insert_db.py`](https://git.esiee.fr/duongh/data-engineering-1/-/blob/master/Projet/insert_db.py), permettant de faire le tri de données et l'insertion dans la base de données MongoDB à l'aide des fichiers jsons qui ont été crawlés.
- Le dossier [`templates`](https://git.esiee.fr/duongh/data-engineering-1/-/tree/master/Projet/templates) concernant les différentes pages de notre plateforme.
- Le dossier [`static`](https://git.esiee.fr/duongh/data-engineering-1/-/tree/master/Projet/static) concernant les différentes images et fonctionnalités de structure de notre plateforme.

Tous ces composants de la structure entière tourneront donc autour d'un fichier principal: `docker-compose.yml`, appelant les différentes technologies que nous utilisons, ici `mongo` en base de données et notre fichier `main.py` comme fichier de compilation central.


# USER'S GUIDE 

## Installation des packages nécessaires
\
Vérifiez tout d'abord si vous disposez de la bonne version de Python. Pour cela:
- ouvrir l'invite de commandes de Windows (Windows+R, puis tapez cmd)
- dans l'invite de commandes tapez `python --version`
- vérifiez si la version est à jour, de préférence la version `3.9.7`

Certains packages seront également nécessaires à installer pour la bonne utilisation du dash si cela n'est pas déjà fait :
- ouvrir l'invite de commandes et se rendre dans le dossier du projet
- Tapez la commande `pip install -r requirements.txt` pour installer les packages nécessaires.
- Tapez la commande `docker compose up -d`, cette commande va permettre de concevoir la technologie MongoDB nécessaire à la plateforme.
- Une fois la commande tapée, démarrer le fichier principal en tapant la commande `python main.py`, une addresse locale va s'ouvrir dans le terminal, il ne reste plus qu"à se rendre  sur cette adresse pour accéder à la plateforme. 


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
- data_s/
  + nos fichiers JSON
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


## First Step: Extraction des données
\
Analysons le fichier `data_scrap.py`. Le début du fichier va tout d'abord les fichiers apparents à la plateforme pour renouveler les données en temps réel en gérant les exceptions des fichiers.
Puis ce fichier va éxécuter des commandes de `scrapy crawl` des fichiers spiders présents dans le dossier `File_crawler`. 
Analysons la structure de ces fichiers, notamment pour le site officiel `formula1.com`. On va tout d'abord définir l'URL de départ, ainsi que le domaine de navigation autorisé, donc tout le site. L'ordre de direction est la suivante:
  - Année de recherche voulue
  - Types de valeurs voulues, ici les données de courses
  - Et quel Grand Prix à étudier

On définit donc les années de 2021 à 2012 (donc décroissante) à étudier et on parcourt après les données de chaque Grand Prix stockées dans des tableaux. 
Ces informations seront stockées sous forme de `scrapy Item` qui seront retournées dans un dictionnaire de valeurs.

On définit ensuite le dossier vers lequel nous allond extraire les données en format `JSON` pour le traitement de la seconde partie.



## Second Step: Traitement et Insertion des données
\
Une fois les données JSON stockées dans notre dossier `data_s`, nous allons les initialiser sous forme de `DataFrames` dans le fichier `insert_db.py` pour le traitement et `merge` certains d'entre eux.

On va notamment gérer certaines exceptions qui se sont passées durant les années 2021, comme l'annulation du Grand Prix de Belgique et donc un problème initial de conversion des données. 

De plus en 2021 a été l'inauguration des courses `Sprint`, ce qui nous a donc obligé à faire des fichiers crawler spécifique pour l'année 2021.

Une fois les fichier enregistrés dans des DataFrames, nous allons tirer les données en renommant les colonnes et valeurs de manière commune, ainsi que changer le format de certaines variables pour pouvoir les moduler plus tard.

Une fois le traitement fini, nous allons les `insérer` dans notre database MongoDB à traver plusieurs collections qui nous serviront à faire nos requêtes. On supprimera au préalable les collections du même nom pour s'assurer de la non-duplication des données. 


## Third Step: Exploitation et affichage des données
\
Nous allons exploiter maintenant notre application à travers le package Flask, un environnement permettant d'avoir plusieurs affichages dynamiquement, contrairement à la technique Dash. 

On va donc pour cela utiliser la methode `render templates` permettant de modifier à travers le fichier principal les templates en html et les données qu'elles retournent. 

On définit pour cela 4 addresses initiales: 
  - la branche initial ('/') qui va générer notre page de bienvenue `hello.html`
  - la branche drivers ('/drivers/"name"') qui affichera les données des pilotes
  - la branche team ('/teams/"name"') celle des équipes
  - la branche grand_prix ('/gps/"name"') celle des Grand Prix

On a donc assimilé à chacun des 3 boutons la redirection vers l'une de ces racines.

Maintenant que nous avons défini les redirections, attaquons-nous aux contenus des différents affichages. 
En fonction du paramètre voulu, nous allons utiliser ce paramètre dans l'attribut `$match` des requêtes MongoDB, et retirer les informations parallèles que nous désirons.

Pour certaines de ces requêtes, nous en avons extrait certaines sous forme de dataframe pour pouvoir faire des représentations graphiques, notamment pour le nombre du pilote et des équipes par saison, et une représentation en `piechart` du type de pneu utilisé le plus fréquent dans un Grand Prix.

Après avoir exploité nos requêtes, il faut maintenant les afficher. L'atout de la technologie Flask est de pouvoir concevoir plusieurs templates en fonction des pages que l'on veut. 
On a pu donc créé plusieurs pages pour cette plateforme et les personnaliser à l'aide d'un fichier css qui nous permet de `customiser` des fonctionnalités de pages comme créer de colonnes de pages ou des lignes complètes, ainsi que les boutons intéractifs que nous avons fait. 













