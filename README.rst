Test du framework Django
Stack : Django 2.2.1 / Python 3 / PostgreSQL

Le but est de récupérer des produits provenant d'un flux xml et de les manipuler.

Chaque tâche doit être faite avec les bonnes pratiques et en respectant la PEP8 :

* Créer un projet Django.
* Créer une app "orders".
* Modèle "Order" reflétant les données présentent dans l'API: http://test.lengow.io/orders-test.xml (4-5 champs suffisent)
* Créer une commande Django permettant de récupérer les commandes de l'API suivante et de les enregistrer en utilisant le modèle "Order".
* Créer les vues nécessaires pour lister les commandes, afficher une commande et rechercher selon les champs du modèle.
* Utiliser Django Rest Framework pour mettre à disposition les commandes précédemment enregistrées en base de données via une API.


INSTALLATION

1) Configuration SGBD :

* Installer Postgres sur le poste
* Avec PgAdmin, créér une base de données lengowTestDP et un utilisateur test/test

2) Initialisation et lancement de l'application :

* cd D:\\django\\lengowTestDP
* python workon lengowTestDP
* python manage.py migrate
* python manage.py runserver

3) Accès a l'application :

* http://127.0.0.1:8000

4) Commande django pour mettre à jour les données à partir de l'API lengow :

* python manage.py updateOrders
