# Gestion-des-Notes
Mini-projet Bases de données

## Objectif du projet

Mettre en place une base de données pour la gestion simplifiée des notes d'élèves d'un collège/lycée.

## Expression des besoins

Plusieurs entretiens ont été réalisés avec des enseignants, des CPE et le proviseur. Il en ressort qu'il faut représenter les concepts de classe (ensemble d'élèves pour une année scolaire donnée pour un niveau donné -exemple 2020/2021 Terminale), de professeur enseignant une ou plusieurs disciplines à différentes classes et d'élèves faisant partie d'une seule classe pour une année donnée et un niveau donné. Chaque discipline donne lieu à une ou plusieurs évaluations et notes à partir desquelles les moyennes par discipline, par trimestre et par année seront calculées. Aucun coefficient n'est appliqué aux notes.

## Fonctionnalités attendues

Les fonctionnalités attendues sont les suivantes :


* Ajout de discipline ;

* Ajout d'enseignants ;

* Ajout d'élèves ;

* Créer les classes chaque année pour chaque niveau ;

* Affecter les notes d'une discipline donnée par un professeur à un élève ;

* Calculer les moyennes et autres statistiques liées aux notes.

## Travail à réaliser

L’ordre des points suivants décrit le travail à réaliser est aussi celui de la réalisation :

1. Proposer une modélisation (MCD) permettant de représenter les besoins décrits précédemment ;
2. Mettre en place la base de données correspondante à l'aide de MySQL ou MariaDB ;
3. Faire un programme, écrit en python ou en PHP via une page web, permettant d'interagir avec la base de données.

## Contenu du rendu

Le rendu sera composé de plusieurs fichiers :


* Une rapide explication sur l’utilisation du logiciel (comment l’installer, le lancer et le tester).

* Un fichier .sql pour la création de votre base de données incluant l’insertion de tuples pour avoir une base initiale de test de façon similaire au fichier createdb_cinema.sql.

* L’ensemble des fichiers de l’application qui exploite votre base de données en nous mentionnant clairement l’utilité de chaque fichier (exemple main.py : fichier principal qui permet de lancer l’application).

* Un document de conception contenant le MCD et le MLD (le MPD étant déjà dans le fichier .sql) ainsi que les DF de chaque objet du MCD/MLD.
