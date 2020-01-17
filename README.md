# Pur Beurre
Ce projet est le huitième réalisé dans le cadre du parcours **OpenClassrooms** ***[Développeur Python](https://openclassrooms.com/fr/paths/68-developpeur-dapplication-python)***.  
Le site est accessible à l'adresse suivante : **[Site PurBeurre](https://purbeurre-nz.herokuapp.com/)**  
Il a été réalisé de manière responsive, pour pouvoir s'adapter à des supports plus petits, tels mobiles ou tablettes.

Ce site est réalisé en langage Python (3.6.8), avec le framework Django. 
Il permet au l'utilisateur de rechercher un aliment de leur choix. Parmi les résultats renvoyés par l'application, il choisi l'aliment dont il souhaite trouver un substitut plus sain. Ainsi, le site affiche à l'utilisateur une proposition de 9 aliments sains. Si l'utilisateur possède un compte et qu'il est authentifié, il a la possibilité d'enregistrer l'aliment en favoris.

## Instalation en local
- Forker ce projet GitHub
- Créer un environnement virtuel à la racine du projet
- Installer les dépendances : *pip install -r requirements.txt*

## Lancement en local
- Il est nécessaire de créer la base de données en local, pour cela exécuter la commande : *./manage.py populate_db*
- Dans la racine du projet, lancer la commande : *./manage.py runserver*
- Se rendre, avec votre navigateur web, à l'adresse suivante : *http://127.0.0.1:8000/*

## APIs utilisés
- ***[OpenFoodFacts](https://en.wiki.openfoodfacts.org/API)***

## Packages utilisés
- **[Django](https://www.djangoproject.com/)** : le framework populaire de Python
- **[Requests](https://requests-fr.readthedocs.io/en/latest/)** : librairie HTTP
- **[Coverage](https://coverage.readthedocs.io/en/coverage-5.0.3/)** : pour la réalisation des tests unitaires

## Lancement des test
A la racine du projet, lancer la commande : *./manage.py test_report*

## Langages web utilisés
- HTML5
- CSS3, avec le framework Bootstrap
- Javascript, avec le framework Jquery

## Template utilisé
- **[Start Boostrap Creative](https://blackrockdigital.github.io/startbootstrap-creative/)**

## Hébergeur utilisé
- **[Heroku](https://www.heroku.com/)**

## Utilisation de l'application
**Recherche d'aliment**
- Ecrire un aliment dans la barre de recherche
- Cliquer sur *Chercher*
- L'application affiche plusieurs résultats :
  - Sélectionner l'aliment à substituer en cliquant sur *Trouver un substitut*
  - Cliquer sur le nom de l'aliment pour une page plus détaillée
- Quand le substitut est sélectionné :
  - Cliquer sur *Ajouter aux favoris* pour l'enregistrer, si l'utilisateur est connecté
  - Sinon il est redirigé vers la page de connexion
  
**Création de compte**
- Cliquer sur l'icone de compte en haut à droite
- Cliquer sur créer un compte utilisateur
- Renseigner les 3 champs :
  - Le nom d'utilisateur ne doit pas être déjà utilisé
  - L'adresse email ne doit pas être déjà utilisée, et doit être au format xxx@xxx.xx
  - Le mot de passe doit avoir un minimum de 8 caractères

**Connexion au compte utilisateur**
- Cliquer sur l'icone de compte en haut à droite
- Renseigner l'identifiant et le mot de passe, puis *Valider*

**Consulter ses favoris**
- Se connecter à son compte utilisateur
- Cliquer sur l'icone de carotte en haut à droit de l'écran

