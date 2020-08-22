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
classe_id int,
PRIMARY KEY (eleve_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


INSERT INTO Eleve (prenom, nom, genre, classe_id) VALUES
('Jean', 'Martin', 'M', 1),
('Pierre', 'Bernard', 'M', 1),
('Michel', 'Thomas', 'M', 1),
('André', 'Petit', 'M', 1),
('Philippe', 'Robert', 'M', 1),
('René', 'Richard', 'M', 1),
('Louis', 'Durand', 'M', 1),
('Alain', 'Dubois', 'M', 1),
('Jacques', 'Moreau', 'M', 1),
('Bernard', 'Laurent', 'M', 1),
('Marcel', 'Simon', 'M', 1),
('Daniel', 'Michel', 'M', 1),
('Roger', 'Lefebvre', 'M', 1),
('Robert', 'Leroy', 'M', 2),
('Paul', 'Roux', 'M', 2),
('Claude', 'David', 'M', 2),
('Christian', 'Bertrand', 'M', 2),
('Henri', 'Morel', 'M', 2),
('Georges', 'Fournier', 'M', 2),
('Nicolas', 'Girard', 'M', 2),
('François', 'Bonnet', 'M', 2),
('Patrick', 'Dupont', 'M', 2),
('Gérard', 'Lambert', 'M', 2),
('Christophe', 'Fontaine', 'M', 2),
('Joseph', 'Rousseau', 'M', 2),
('Julien', 'Vincent', 'M', 2),
('Mauric', 'Muller', 'M', 3),
('Laurent', 'Lefevre', 'M', 3),
('Frédéric', 'Faure', 'M', 3),
('Eric', 'Andre', 'M', 3),
('David', 'Mercier', 'M', 3),
('Stéphane', 'Blanc', 'M', 3),
('Pascal', 'Guerin', 'M', 3),
('Sébastien', 'Boyer', 'M', 3),
('Alexandre', 'Garnier', 'M', 3),
('Thierry', 'Chevalier', 'M', 3),
('Olivier', 'Francois', 'M', 3),
('Thomas', 'Legrand', 'M', 3),
('Antoine', 'Gauthier', 'M', 3),
('Raymond', 'Garcia', 'M', 4),
('Guy', 'Perrin', 'M', 4),
('Dominique', 'Robin', 'M', 4),
('Charles', 'Clement', 'M', 4),
('Didier', 'Morin', 'M', 4),
('Marc', 'Nicolas', 'M', 4),
('Vincent', 'Henry', 'M', 4),
('Yves', 'Roussel', 'M', 4),
('Guillaume', 'Mathieu', 'M', 4),
('Bruno', 'Gautier', 'M', 4),
('Serge', 'Masson', 'M', 4),
('Maxime', 'Marchand', 'M', 4),
('Lucien', 'Duval', 'M', 5),
('Jean', 'Denis', 'M', 5),
('Albert', 'Dumont', 'M', 5),
('Romain', 'Marie', 'M', 5),
('Jerome', 'Lemaire', 'M', 5),
('Gilbert', 'Noel', 'M', 5),
('Franck', 'Meyer', 'M', 5),
('Gilles', 'Dufour', 'M', 5),
('Gabriel', 'Meunier', 'M', 5),
('Anthony', 'Brun', 'M', 5),
('Jean', 'Blanchard', 'M', 5),
('Clément', 'Giraud', 'M', 5),
('Francis', 'Joly', 'M', 6),
('Emile', 'Riviere', 'M', 6),
('Lucas', 'Lucas', 'M', 6),
('Denis', 'Brunet', 'M', 6),
('Kevin', 'Gaillard', 'M', 6),
('Mathieu', 'Barbier', 'M', 6),
('Jules', 'Arnaud', 'M', 6),
('Benjamin', 'Martinez', 'M', 6),
('Alexis', 'Gerard', 'M', 6),
('Joël', 'Roche', 'M', 6),
('Hervé', 'Renard', 'M', 6),
('Patrice', 'Schmitt', 'M', 6),
('Sylvain', 'Roy', 'M', 7),
('Hugo', 'Leroux', 'M', 7),
('Emmanuel', 'Colin', 'M', 7),
('Adrien', 'Vidal', 'M', 7),
('Fabrice', 'Caron', 'M', 7),
('Arnaud', 'Picard', 'M', 7),
('Cedric', 'Roger', 'M', 7),
('Roland', 'Fabre', 'M', 7),
('Raphaël', 'Aubert', 'M', 7),
('Florian', 'Lemoine', 'M', 7),
('Quentin', 'Renaud', 'M', 7),
('Ludovic', 'Dumas', 'M', 7),
('Damien', 'Lacroix', 'M', 8),
('Benoît', 'Olivier', 'M', 8),
('Victor', 'Philippe', 'M', 8),
('Fernand', 'Bourgeois', 'M', 8),
('Léon', 'Pierre', 'M', 8),
('Jeremy', 'Benoit', 'M', 8),
('Jean', 'Rey', 'M', 8),
('Arthur', 'Leclerc', 'M', 8),
('Théo', 'Payet', 'M', 8),
('Xavier', 'Rolland', 'M', 8),
('Fabien', 'Leclercq', 'M', 8),
('Enzo', 'Guillaume', 'M', 8),
('Mickael', 'Lecomte', 'M', 9),
('Marie', 'Lopez', 'F', 9),
('Jeanne', 'Jean', 'F', 9),
('Françoise', 'Dupuy', 'F', 9),
('Monique', 'Guillot', 'F', 9),
('Nathalie', 'Hubert', 'F', 9),
('Isabelle', 'Berger', 'F', 9),
('Jacqueline', 'Carpentier', 'F', 9),
('Anne', 'Sanchez', 'F', 9),
('Sylvie', 'Dupuis', 'F', 9),
('Martine', 'Moulin', 'F', 9),
('Madeleine', 'Louis', 'F', 9),
('Nicole', 'Deschamps', 'F', 10),
('Suzanne', 'Huet', 'F', 10),
('Hélène', 'Vasseur', 'F', 10),
('Christine', 'Perez', 'F', 10),
('Denise', 'Boucher', 'F', 10),
('Louise', 'Fleury', 'F', 10),
('Christiane', 'Royer', 'F', 10),
('Valérie', 'Klein', 'F', 10),
('Sophie', 'Jacquet', 'F', 10),
('Stéphanie', 'Adam', 'F', 10),
('Céline', 'Paris', 'F', 10),
('Véronique', 'Poirier', 'F', 11),
('Chantal', 'Marty', 'F', 11),
('Renée', 'Aubry', 'F', 11),
('Simone', 'Guyot', 'F', 11),
('Andrée', 'Carre', 'F', 11),
('Germaine', 'Charles', 'F', 11),
('Annie', 'Renault', 'F', 11),
('Patricia', 'Charpentier', 'F', 11),
('Yvette', 'Menard', 'F', 11),
('Brigitte', 'Maillard', 'F', 11),
('Lucie', 'Baron', 'F', 11),
('Léa', 'Bertin', 'F', 11),
('Odette', 'Bailly', 'F', 11),
('Emilie', 'Herve', 'F', 11),
('Alice', 'Schneider', 'F', 11),
('Laurence', 'Fernandez', 'F', 11),
('Michèle', 'Collet', 'F', 11),
('Cécile', 'Leger', 'F', 11),
('Thérèse', 'Bouvier', 'F', 11),
('Virginie', 'Julien', 'F', 11),
('Lucienne', 'Prevost', 'F', 11),
('Dominique', 'Millet', 'F', 11),
('Sarah', 'Perrot', 'F', 12),
('Raymonde', 'Daniel', 'F', 12),
('Manon', 'Cousin', 'F', 12),
('Corinne', 'Germain', 'F', 12),
('Elisabeth', 'Breton', 'F', 12),
('Claire', 'Besson', 'F', 12),
('Claudine', 'Langlois', 'F', 12),
('Danielle', 'Remy', 'F', 12),
('Elodie', 'Pelletier', 'F', 12),
('Caroline', 'Leveque', 'F', 12),
('Pauline', 'Perrier', 'F', 12),
('Christelle', 'Leblanc', 'F', 12),
('Josette', 'Barre', 'F', 12),
('Emma', 'Lebrun', 'F', 12),
('Florence', 'Marchal', 'F', 1),
('Laura', 'Weber', 'F', 1),
('Charlotte', 'Mallet', 'F', 1),
('Chloé', 'Hamon', 'F', 1),
('Bernadette', 'Boulanger', 'F', 1),
('Audrey', 'Jacob', 'F', 1),
('Maria', 'Monnier', 'F', 1),
('Gisèle', 'Michaud', 'F', 1),
('Mélanie', 'Rodriguez', 'F', 1),
('Laetitia', 'Guichard', 'F', 1),
('Ginette', 'Gillet', 'F', 1),
('Annick', 'Etienne', 'F', 1),
('Nadine', 'Grondin', 'F', 1),
('Béatrice', 'Poulain', 'F', 1),
('Mireille', 'Tessier', 'F', 1),
('Anaïs', 'Chevallier', 'F', 2),
('Evelyne', 'Collin', 'F', 2),
('Delphine', 'Chauvin', 'F', 2),
('Henriette', 'Da', 'F', 2),
('Marion', 'Bouchet', 'F', 2),
('Marthe', 'Lemaitre', 'F', 2),
('Michelle', 'Benard', 'F', 2),
('Karine', 'Marechal', 'F', 2),
('Marine', 'Humbert', 'F', 2),
('Elise', 'Reynaud', 'F', 2),
('Eliane', 'Antoine', 'F', 2);

show warnings;

-- ------------------------------------------------
-- Création de la table Classe
CREATE or replace TABLE Classe (
classe_id int NOT NULL AUTO_INCREMENT,
nom varchar(20) COLLATE utf8_bin NOT NULL,
niveau varchar(20) COLLATE utf8_bin DEFAULT NULL,
annee_id int,
PRIMARY KEY (classe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Classe (nom, niveau, annee_id) VALUES
('S1', 'seconde', 1),
('S2', 'seconde', 1),
('S3', 'seconde', 1),
('S4', 'seconde', 1),
('S5', 'seconde', 1),
('P1', 'Première', 1),
('P2', 'Première', 1),
('P3', 'Première', 1),
('P4', 'Première', 1),
('P5', 'Première', 1),
('T1', 'Terminale', 1),
('T2', 'Terminale', 1),
('T3', 'Terminale', 1),
('T4', 'Terminale', 1),
('T5', 'Terminale', 1);




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
('semestre 2');



-- ------------------------------------------------
-- Création de la table AnneeScolaire

CREATE OR replace TABLE Anneescolaire (
  annee_id int NOT NULL AUTO_INCREMENT,
  nom VARCHAR(20) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`annee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO Anneescolaire (nom) VALUES
('2019-2020'),
('2020-2021');

-- ------------------------------------------------
-- Clés étrangères
-- ALTER TABLE Enseigner ADD FOREIGN KEY (discipline_id) REFERENCES Discipline (discipline_id);
-- ALTER TABLE Enseigner ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);
-- ALTER TABLE Enseigner ADD FOREIGN KEY (professeur_id) REFERENCES Professeur (professeur_id);
-- ALTER TABLE Evaluation ADD FOREIGN KEY (periode_id) REFERENCES Periode (periode_id);
-- ALTER TABLE Evaluation ADD FOREIGN KEY (annee_id) REFERENCES Anneescolaire (annee_id);
-- ALTER TABLE Evaluation ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);
-- ALTER TABLE Evaluation ADD FOREIGN KEY (professeur_id) REFERENCES Professeur (professeur_id);
-- ALTER TABLE Evaluation ADD FOREIGN KEY (discipline_id) REFERENCES Discipline (discipline_id);
ALTER TABLE Classe ADD FOREIGN KEY (annee_id) REFERENCES Anneescolaire (annee_id);
-- ALTER TABLE Evaluer ADD FOREIGN KEY (eleve_id) REFERENCES Eleve (eleve_id);
-- ALTER TABLE Evaluer ADD FOREIGN KEY (evaluation_id) REFERENCES Evaluation (evaluation_id);
ALTER TABLE Eleve ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);







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
