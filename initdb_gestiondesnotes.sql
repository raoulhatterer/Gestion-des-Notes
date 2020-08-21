-- ------------------------------------------------
-- Pour exécuter le script sql d'initialisation
-- À partir du Terminal se rendre dans le dossier où se trouve le script
-- Se connecter en tant que root à mysql avec
-- mysql -u root -p
-- Dans l'invite de commande MariaDB> entrer:
-- SOURCE ./initdb_gestiondesnotes.sql;


-- ------------------------------------------------
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+01:00";

-- ------------------------------------------------
-- Création de la base de données
-- Efface l'ancienne bd si elle existait
-- et en crée une nouvelle
CREATE OR REPLACE DATABASE bd_gestion_des_notes;
USE bd_gestion_des_notes;

-- ------------------------------------------------
-- Création de différents rôles
CREATE OR replace ROLE role_gestionnaire;
GRANT ALL 
ON bd_gestion_des_notes.* 
TO role_gestionnaire;

-- CREATE ROLE role_personnel;
-- GRANT CREATE TABLE, CREATE VIEW
-- TO user_personnel;

-- CREATE ROLE role_professeur;
-- GRANT CREATE VIEW
-- TO role_professeur;

-- CREATE ROLE role_eleve;
-- GRANT CREATE VIEW
-- TO role_eleve;


-- ------------------------------------------------
-- Création de différents utilisateurs

CREATE OR replace USER  stil@localhost IDENTIFIED BY 'stilstil';                 
GRANT role_gestionnaire
TO stil@localhost;
SET DEFAULT ROLE role_gestionnaire FOR stil@localhost;

CREATE OR replace USER  proviseur@localhost IDENTIFIED BY 'propro';                 
GRANT role_gestionnaire
TO proviseur@localhost;
SET DEFAULT ROLE role_gestionnaire FOR proviseur@localhost;

-- CREATE OR replace USER  first_connection@localhost       
-- IDENTIFIED BY 'first_connection';                 
-- GRANT SELECT ON Administrateurs
-- TO first_connection@localhost;
-- GRANT SELECT ON Professeurs
-- TO first_connection@localhost;
-- GRANT SELECT ON Eleves
-- TO first_connection@localhost;
-- GRANT CREATE VIEW ON bd_gestion_des_notes.*
-- TO first_connection@localhost;
-- GRANT DROP ON bd_gestion_des_notes.*
-- TO first_connection@localhost;


-- FLUSH PRIVILEGES;






-- ------------------------------------------------
-- Création de la table des fonctions
-- des gestionnaires de la base de données
CREATE TABLE IF NOT EXISTS Fonctions(
Func_Id varchar(10) COLLATE utf8_bin NOT NULL,
Func_Name varchar(30) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (Func_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Fonctions (Func_Id, Func_Name) VALUES
('P1', 'Proviseur'),
('P2', 'Proviseur-adjoint'),
('S', 'Secrétaire de direction'),
('ST', 'STIL'),
('Prof', 'Professeur'),
('E', 'Élève'),
('Par', 'Parent'),
('A', 'Agent'),
('C', 'CPE');

show warnings;
-- ------------------------------------------------
-- Création de la table du personnel non enseignant
CREATE TABLE IF NOT EXISTS Administrateurs(
Admin_Id int NOT NULL AUTO_INCREMENT,
FirstName varchar(30) COLLATE utf8_bin DEFAULT NULL,
LastName varchar(30) COLLATE utf8_bin DEFAULT NULL,
Func_Id varchar(5) COLLATE utf8_bin NOT NULL,
Gender char DEFAULT NULL,
Birthday DATE,
Login varchar(30) COLLATE utf8_bin DEFAULT NULL,
PRIMARY KEY (Admin_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Administrateurs(FirstName, LastName, Func_Id, Gender, Birthday, Login) VALUES
('Prénom', 'Nom', 'P1', 'M', '1966-04-20',  'proviseur'),
('Raoul', 'Hatterer', 'ST', 'M', '1966-04-20',  'stil');

show warnings;
-- ------------------------------------------------
-- Création de la table Professeur
CREATE TABLE IF NOT EXISTS Professeur (
professeur_id int NOT NULL AUTO_INCREMENT,
prenom varchar(40) COLLATE utf8_bin NOT NULL,
nom varchar(30) COLLATE utf8_bin NOT NULL,
titre char DEFAULT NULL,
PRIMARY KEY (professeur_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Professeur (prenom, nom, titre) VALUES
('Kunihiko', 'Kodaira', 'M'),
('Pierre', 'Serre', 'M'),
('Klaus', 'Roth', 'M'),
('René', 'Thom', 'M'),
('Lars', 'Hörmander', 'M'),
('John', 'Milnor', 'M'),
('Michael', 'Atiyah', 'M'),
('Paul', 'Cohen', 'M'),
('Alexandre', 'Grothendieckd', 'M'),
('Stephen', 'Smale', 'M'),
('Alan', 'Baker', 'M'),
('Heisuke', 'Hironaka', 'M'),
('Sergueï', 'Novikov', 'M'),
('Griggs', 'Thompson', 'M'),
('Enrico', 'Bombieri', 'M'),
('David', 'Mumford', 'M'),
('Pierre', 'Deligne', 'M'),
('Charles', 'Fefferman', 'M'),
('Gregori', 'Margulis', 'M'),
('Daniel', 'Quillen', 'M'),
('Alain', 'Connes', 'M'),
('William', 'Thurston', 'M'),
('Tung', 'Yaue', 'M'),
('Simon', 'Donaldson', 'M'),
('Gerd', 'Faltings', 'M'),
('Michael', 'Freedman', 'M'),
('Vladimir', 'Drinfeld', 'M'),
('Vaughan', 'Jones', 'M'),
('Shigefumi', 'Mori', 'M'),
('Edward', 'Witten', 'M'),
('Jean', 'Bourgain', 'M'),
('Louis', 'Lions', 'M'),
('Christophe', 'Yoccoz', 'M'),
('Efim', 'Zelmanov', 'M'),
('Ewen', 'Borcherds', 'M'),
('Timothy', 'Gowers', 'M'),
('Maxim', 'Kontsevich', 'M'),
('Curtis', 'McMullen', 'M'),
('Laurent', 'Lafforgue', 'M'),
('Vladimir', 'Voevodsky', 'M'),
('Andreï', 'Okounkov', 'M'),
('Terence', 'Tao', 'M'),
('Wendelin', 'Werner', 'M'),
('Elon', 'Lindenstrauss', 'M'),
('Bảo', 'Châu', 'M'),
('Stanislav', 'Smirnov', 'M'),
('Cédric', 'Villani', 'M'),
('Artur', 'Ávila', 'M'),
('Manjul', 'Bhargava', 'M'),
('Martin', 'Hairer', 'M'),
('Maryam', 'Mirzakhani', 'F'),
('Caucher', 'Birkar', 'M'),
('Alessio', 'Figalli', 'M'),
('Peter', 'Scholze', 'M'),
('Akshay', 'Venkatesh', 'M'),
('Marie', 'Curie', 'F'),
('Irène', 'Joliot-Curie', 'F'),
('Gerty', 'Cori', 'F'),
('Maria', 'Goeppert-Mayer', 'F'),
('Dorothy', 'Crowfoot-Hodgkin', 'F'),
('Rosalyn', 'Yalow', 'F'),
('Barbara', 'McClintock', 'F'),
('Rita', 'Levi-Montalcini', 'F'),
('Gertrude', 'Elion', 'F'),
('Christiane', 'Nüsslein-Volhard', 'F'),
('Linda', 'Buck', 'F'),
('Françoise', 'Barré-Sinoussi', 'F'),
('Elizabeth', 'Blackburn', 'F'),
('Carol', 'Greider', 'F'),
('Ada', 'Yonath', 'F'),
('May-Britt', 'Moser', 'F'),
('Youyou', 'Tu', 'F');

show warnings;



-- ------------------------------------------------
-- Création de la table Discipline
CREATE or replace TABLE Discipline (
discipline_id int NOT NULL AUTO_INCREMENT,
Disc_Name varchar(50) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (discipline_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Discipline (Disc_Name) VALUES
('À définir'),
('Histoire - Géographie'),
('Sciences économiques et sociales'),
('Sciences de la vie et de la Terre'),
('Education physique et sportive'),
('Enseignement moral et civique'),
('Sciences numériques et technologie'),
('Français'),
('Mathématiques'),
('NSI'),
('Physique-Chimie');

show warnings;

-- ------------------------------------------------
-- Création de la table Élève
CREATE TABLE IF NOT EXISTS Eleve (
eleve_id int NOT NULL AUTO_INCREMENT,
prenom varchar(20) COLLATE utf8_bin NOT NULL,
nom varchar(20) COLLATE utf8_bin NOT NULL,
genre varchar(10) COLLATE utf8_bin DEFAULT NULL,
classe_id varchar(10) COLLATE utf8_bin DEFAULT NULL,
PRIMARY KEY (eleve_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO Eleve (prenom, nom, genre) VALUES
('Jean', 'Martin', 'M'),
('Pierre', 'Bernard', 'M'),
('Michel', 'Thomas', 'M'),
('André', 'Petit', 'M'),
('Philippe', 'Robert', 'M'),
('René', 'Richard', 'M'),
('Louis', 'Durand', 'M'),
('Alain', 'Dubois', 'M'),
('Jacques', 'Moreau', 'M'),
('Bernard', 'Laurent', 'M'),
('Marcel', 'Simon', 'M'),
('Daniel', 'Michel', 'M'),
('Roger', 'Lefebvre', 'M'),
('Robert', 'Leroy', 'M'),
('Paul', 'Roux', 'M'),
('Claude', 'David', 'M'),
('Christian', 'Bertrand', 'M'),
('Henri', 'Morel', 'M'),
('Georges', 'Fournier', 'M'),
('Nicolas', 'Girard', 'M'),
('François', 'Bonnet', 'M'),
('Patrick', 'Dupont', 'M'),
('Gérard', 'Lambert', 'M'),
('Christophe', 'Fontaine', 'M'),
('Joseph', 'Rousseau', 'M'),
('Julien', 'Vincent', 'M'),
('Mauric', 'Muller', 'M'),
('Laurent', 'Lefevre', 'M'),
('Frédéric', 'Faure', 'M'),
('Eric', 'Andre', 'M'),
('David', 'Mercier', 'M'),
('Stéphane', 'Blanc', 'M'),
('Pascal', 'Guerin', 'M'),
('Sébastien', 'Boyer', 'M'),
('Alexandre', 'Garnier', 'M'),
('Thierry', 'Chevalier', 'M'),
('Olivier', 'Francois', 'M'),
('Thomas', 'Legrand', 'M'),
('Antoine', 'Gauthier', 'M'),
('Raymond', 'Garcia', 'M'),
('Guy', 'Perrin', 'M'),
('Dominique', 'Robin', 'M'),
('Charles', 'Clement', 'M'),
('Didier', 'Morin', 'M'),
('Marc', 'Nicolas', 'M'),
('Vincent', 'Henry', 'M'),
('Yves', 'Roussel', 'M'),
('Guillaume', 'Mathieu', 'M'),
('Bruno', 'Gautier', 'M'),
('Serge', 'Masson', 'M'),
('Maxime', 'Marchand', 'M'),
('Lucien', 'Duval', 'M'),
('Jean', 'Denis', 'M'),
('Albert', 'Dumont', 'M'),
('Romain', 'Marie', 'M'),
('Jerome', 'Lemaire', 'M'),
('Gilbert', 'Noel', 'M'),
('Franck', 'Meyer', 'M'),
('Gilles', 'Dufour', 'M'),
('Gabriel', 'Meunier', 'M'),
('Anthony', 'Brun', 'M'),
('Jean', 'Blanchard', 'M'),
('Clément', 'Giraud', 'M'),
('Francis', 'Joly', 'M'),
('Emile', 'Riviere', 'M'),
('Lucas', 'Lucas', 'M'),
('Denis', 'Brunet', 'M'),
('Kevin', 'Gaillard', 'M'),
('Mathieu', 'Barbier', 'M'),
('Jules', 'Arnaud', 'M'),
('Benjamin', 'Martinez', 'M'),
('Alexis', 'Gerard', 'M'),
('Joël', 'Roche', 'M'),
('Hervé', 'Renard', 'M'),
('Patrice', 'Schmitt', 'M'),
('Sylvain', 'Roy', 'M'),
('Hugo', 'Leroux', 'M'),
('Emmanuel', 'Colin', 'M'),
('Adrien', 'Vidal', 'M'),
('Fabrice', 'Caron', 'M'),
('Arnaud', 'Picard', 'M'),
('Cedric', 'Roger', 'M'),
('Roland', 'Fabre', 'M'),
('Raphaël', 'Aubert', 'M'),
('Florian', 'Lemoine', 'M'),
('Quentin', 'Renaud', 'M'),
('Ludovic', 'Dumas', 'M'),
('Damien', 'Lacroix', 'M'),
('Benoît', 'Olivier', 'M'),
('Victor', 'Philippe', 'M'),
('Fernand', 'Bourgeois', 'M'),
('Léon', 'Pierre', 'M'),
('Jeremy', 'Benoit', 'M'),
('Jean', 'Rey', 'M'),
('Arthur', 'Leclerc', 'M'),
('Théo', 'Payet', 'M'),
('Xavier', 'Rolland', 'M'),
('Fabien', 'Leclercq', 'M'),
('Enzo', 'Guillaume', 'M'),
('Mickael', 'Lecomte', 'M'),
('Marie', 'Lopez', 'F'),
('Jeanne', 'Jean', 'F'),
('Françoise', 'Dupuy', 'F'),
('Monique', 'Guillot', 'F'),
('Nathalie', 'Hubert', 'F'),
('Isabelle', 'Berger', 'F'),
('Jacqueline', 'Carpentier', 'F'),
('Anne', 'Sanchez', 'F'),
('Sylvie', 'Dupuis', 'F'),
('Martine', 'Moulin', 'F'),
('Madeleine', 'Louis', 'F'),
('Nicole', 'Deschamps', 'F'),
('Suzanne', 'Huet', 'F'),
('Hélène', 'Vasseur', 'F'),
('Christine', 'Perez', 'F'),
('Denise', 'Boucher', 'F'),
('Louise', 'Fleury', 'F'),
('Christiane', 'Royer', 'F'),
('Valérie', 'Klein', 'F'),
('Sophie', 'Jacquet', 'F'),
('Stéphanie', 'Adam', 'F'),
('Céline', 'Paris', 'F'),
('Véronique', 'Poirier', 'F'),
('Chantal', 'Marty', 'F'),
('Renée', 'Aubry', 'F'),
('Simone', 'Guyot', 'F'),
('Andrée', 'Carre', 'F'),
('Germaine', 'Charles', 'F'),
('Annie', 'Renault', 'F'),
('Patricia', 'Charpentier', 'F'),
('Yvette', 'Menard', 'F'),
('Brigitte', 'Maillard', 'F'),
('Lucie', 'Baron', 'F'),
('Léa', 'Bertin', 'F'),
('Odette', 'Bailly', 'F'),
('Emilie', 'Herve', 'F'),
('Alice', 'Schneider', 'F'),
('Laurence', 'Fernandez', 'F'),
('Michèle', 'Collet', 'F'),
('Cécile', 'Leger', 'F'),
('Thérèse', 'Bouvier', 'F'),
('Virginie', 'Julien', 'F'),
('Lucienne', 'Prevost', 'F'),
('Dominique', 'Millet', 'F'),
('Sarah', 'Perrot', 'F'),
('Raymonde', 'Daniel', 'F'),
('Manon', 'Cousin', 'F'),
('Corinne', 'Germain', 'F'),
('Elisabeth', 'Breton', 'F'),
('Claire', 'Besson', 'F'),
('Claudine', 'Langlois', 'F'),
('Danielle', 'Remy', 'F'),
('Elodie', 'Pelletier', 'F'),
('Caroline', 'Leveque', 'F'),
('Pauline', 'Perrier', 'F'),
('Christelle', 'Leblanc', 'F'),
('Josette', 'Barre', 'F'),
('Emma', 'Lebrun', 'F'),
('Florence', 'Marchal', 'F'),
('Laura', 'Weber', 'F'),
('Charlotte', 'Mallet', 'F'),
('Chloé', 'Hamon', 'F'),
('Bernadette', 'Boulanger', 'F'),
('Audrey', 'Jacob', 'F'),
('Maria', 'Monnier', 'F'),
('Gisèle', 'Michaud', 'F'),
('Mélanie', 'Rodriguez', 'F'),
('Laetitia', 'Guichard', 'F'),
('Ginette', 'Gillet', 'F'),
('Annick', 'Etienne', 'F'),
('Nadine', 'Grondin', 'F'),
('Béatrice', 'Poulain', 'F'),
('Mireille', 'Tessier', 'F'),
('Anaïs', 'Chevallier', 'F'),
('Evelyne', 'Collin', 'F'),
('Delphine', 'Chauvin', 'F'),
('Henriette', 'Da', 'F'),
('Marion', 'Bouchet', 'F'),
('Marthe', 'Lemaitre', 'F'),
('Michelle', 'Benard', 'F'),
('Karine', 'Marechal', 'F'),
('Marine', 'Humbert', 'F'),
('Elise', 'Reynaud', 'F'),
('Eliane', 'Antoine', 'F');

show warnings;

-- ------------------------------------------------
-- Création de la table Classe
CREATE or replace TABLE Classe (
classe_id int NOT NULL AUTO_INCREMENT,
nom varchar(20) COLLATE utf8_bin NOT NULL,
niveau varchar(20) COLLATE utf8_bin DEFAULT NULL,
annee_id varchar(20) COLLATE utf8_bin DEFAULT NULL,
PRIMARY KEY (classe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Classe (nom, niveau, annee_id) VALUES
('S1', 'seconde', '2019-2020'),
('À définir', 'À définir', '2019-2020');



-- ------------------------------------------------
-- Création de la table Periode

CREATE OR replace TABLE Periode (
  periode_id int NOT NULL AUTO_INCREMENT,
  nom VARCHAR(20) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (periode_id) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO Periode (nom) VALUES
('trimestre 1'),
('trimestre 2'),
('trimestre 3'),
('semestre 1'),
('semestre 2'),
('À définir');


-- ------------------------------------------------
-- Création de la table AnneeScolaire

CREATE TABLE Anneescolaire (
  annee_id int NOT NULL AUTO_INCREMENT,
  nom VARCHAR(20) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`annee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO Anneescolaire (nom) VALUES
('2019-2020'),
('2020-2021'),
('À définir');



-- ------------------------------------------------
-- DESCRIPTIONS
SELECT "TABLES";
SHOW tables;
SELECT "Description de la TABLE Discipline";
DESCRIBE Discipline;
SELECT * FROM Discipline;
SELECT "Description de la TABLE des Fonctions du personnel";
DESCRIBE Fonctions;
SELECT * FROM Fonctions;
SELECT "Description de la TABLE Administrateurs";
DESCRIBE Administrateurs;
SELECT * FROM Administrateurs;
SELECT "Description de la TABLE Professeur";
DESCRIBE Professeur;
SELECT * FROM Professeur;
SELECT "Description de la TABLE Eleve";
DESCRIBE Eleve;
SELECT * FROM Eleve;
SELECT "Description de la TABLE Classe";
DESCRIBE Classe;
SELECT * FROM Classe;
SELECT "Description de la TABLE Periode";
DESCRIBE Periode;
SELECT * FROM Periode;
SELECT "Description de la TABLE Anneescolaire";
DESCRIBE Anneescolaire;
SELECT * FROM Anneescolaire;

SELECT "UTILISATEURS";
select host, USER, password from mysql.user;
