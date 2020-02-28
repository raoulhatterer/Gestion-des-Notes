SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+01:00";

-- ------------------------------------------------
-- Reset: efface l'ancienne bd si elle existait
-- et en crée une nouvelle
CREATE OR REPLACE DATABASE bd_gestion_des_notes;
USE bd_gestion_des_notes;
-- ------------------------------------------------
-- Création de la table des fonctions
-- des gestionnaires de la base de données
CREATE TABLE IF NOT EXISTS Fonctions(
Func_Id  int(10),
Func_Name varchar(20) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (Func_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Fonctions (Func_Id, Func_Name) VALUES
(1, 'Proviseur'),
(2, 'Proviseur-adjoint'),
(3, 'Secrétaire de direction'),
(4, 'STIL');

-- ------------------------------------------------
-- Création de la table du personnel
CREATE TABLE IF NOT EXISTS Personnel(
Pers_Id int NOT NULL AUTO_INCREMENT,
FirstName varchar(20) COLLATE utf8_bin DEFAULT NULL,
LastName varchar(20) COLLATE utf8_bin DEFAULT NULL,
Func_Id int,
Gender char DEFAULT NULL,
Birthday date,
Password varchar(20) COLLATE utf8_bin DEFAULT NULL,
Droit_Admin BOOLEAN DEFAULT FALSE NOT NULL,
PRIMARY KEY (Pers_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Personnel(FirstName, LastName, Func_Id, Gender, Droit_Admin, Password) VALUES
('Lars', 'Ahlfors', 1, 'M', TRUE, 'Proviseur'),              
('Jesse', 'Douglas', 2, 'M', TRUE, 'Proviseur-adjoint'),      
('Laurent', 'Schwartz', 3, 'M', TRUE, 'Secrétaire de direction'),
('Atle', 'Selberg', 4, 'M', TRUE, 'stil');

-- ------------------------------------------------
-- Création de la table professeurs
CREATE TABLE IF NOT EXISTS Professeurs (
Prof_Id int NOT NULL AUTO_INCREMENT,
FirstName varchar(20) COLLATE utf8_bin NOT NULL,
LastName varchar(20) COLLATE utf8_bin NOT NULL,
Disc_Id int,
Gender char DEFAULT NULL,
Birthday date,
Grade_Id int DEFAULT NULL,
Password varchar(20) COLLATE utf8_bin DEFAULT NULL,
Droit_Admin BOOLEAN DEFAULT FALSE NOT NULL,
PRIMARY KEY (Prof_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Professeurs (FirstName, LastName, Disc_Id, Gender) VALUES
('Kunihiko', 'Kodaira', 2, 'M'),
('Pierre', 'Serre', 3, 'M'),
('Klaus', 'Roth', 4, 'M'),
('René', 'Thom', 5, 'M'),
('Lars', 'Hörmander', 2, 'M'),
('John', 'Milnor', 3, 'M'),
('Michael', 'Atiyah', 4, 'M'),
('Paul', 'Cohen', 5, 'M'),
('Alexandre', 'Grothendieckd', 2, 'M'),
('Stephen', 'Smale', 3, 'M'),
('Alan', 'Baker', 4, 'M'),
('Heisuke', 'Hironaka', 5, 'M'),
('Sergueï', 'Novikov', 2, 'M'),
('Griggs', 'Thompson', 3, 'M'),
('Enrico', 'Bombieri', 4, 'M'),
('David', 'Mumford', 5, 'M'),
('Pierre', 'Deligne', 2, 'M'),
('Charles', 'Fefferman', 3, 'M'),
('Gregori', 'Margulis', 4, 'M'),
('Daniel', 'Quillen', 5, 'M'),
('Alain', 'Connes', 2, 'M'),
('William', 'Thurston', 3, 'M'),
('Tung', 'Yaue', 4, 'M'),
('Simon', 'Donaldson', 5, 'M'),
('Gerd', 'Faltings', 2, 'M'),
('Michael', 'Freedman', 3, 'M'),
('Vladimir', 'Drinfeld', 4, 'M'),
('Vaughan', 'Jones', 5, 'M'),
('Shigefumi', 'Mori', 2, 'M'),
('Edward', 'Witten', 3, 'M'),
('Jean', 'Bourgain', 4, 'M'),
('Louis', 'Lions', 5, 'M'),
('Christophe', 'Yoccoz', 2, 'M'),
('Efim', 'Zelmanov', 3, 'M'),
('Ewen', 'Borcherds', 4, 'M'),
('Timothy', 'Gowers', 5, 'M'),
('Maxim', 'Kontsevich', 2, 'M'),
('Curtis', 'McMullen', 3, 'M'),
('Laurent', 'Lafforgue', 4, 'M'),
('Vladimir', 'Voevodsky', 5, 'M'),
('Andreï', 'Okounkov', 2, 'M'),
('Terence', 'Tao', 3, 'M'),
('Wendelin', 'Werner', 4, 'M'),
('Elon', 'Lindenstrauss', 5, 'M'),
('Bảo', 'Châu', 2, 'M'),
('Stanislav', 'Smirnov', 3, 'M'),
('Cédric', 'Villani', 4, 'M'),
('Artur', 'Ávila', 5, 'M'),
('Manjul', 'Bhargava', 2, 'M'),
('Martin', 'Hairer', 3, 'M'),
('Maryam', 'Mirzakhani', 4, 'F'),
('Caucher', 'Birkar', 5, 'M'),
('Alessio', 'Figalli', 2, 'M'),
('Peter', 'Scholze', 3, 'M'),
('Akshay', 'Venkatesh', 4, 'M'),
('Marie', 'Curie', 2, 'F'),
('Irène', 'Joliot-Curie', 3, 'F'),
('Gerty', 'Cori', 4, 'F'),
('Maria', 'Goeppert-Mayer', 5, 'F'),
('Dorothy', 'Crowfoot-Hodgkin', 2, 'F'),
('Rosalyn', 'Yalow', 3, 'F'),
('Barbara', 'McClintock', 4, 'F'),
('Rita', 'Levi-Montalcini', 5, 'F'),
('Gertrude', 'Elion', 2, 'F'),
('Christiane', 'Nüsslein-Volhard', 3, 'F'),
('Linda', 'Buck', 4, 'F'),
('Françoise', 'Barré-Sinoussi', 5, 'F'),
('Elizabeth', 'Blackburn', 2, 'F'),
('Carol', 'Greider', 3, 'F'),
('Ada', 'Yonath', 4, 'F'),
('May-Britt', 'Moser', 5, 'F'),
('Youyou', 'Tu', 2, 'F');



-- ------------------------------------------------
-- Création de la table disciplines
CREATE or replace TABLE Disciplines (
Disc_Id int NOT NULL AUTO_INCREMENT,
Disc_Name varchar(20) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (Disc_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Disciplines (Disc_Name) VALUES
('À définir'),
('Français'),
('Mathématiques'),
('NSI'),
('Physique-Chimie');


-- ------------------------------------------------
-- Création de différents utilisateurs
CREATE OR REPLACE USER user_gestionnaire@localhost
IDENTIFIED BY 'gestionnaire';
GRANT ALL PRIVILEGES ON bd_gestion_des_notes.* 
TO user_gestionnaire@localhost;

CREATE OR replace USER  user_stil@localhost       
IDENTIFIED BY 'stil';                 
GRANT ALL PRIVILEGES ON bd_gestion_des_notes.*
TO user_stil@localhost;

-- ------------------------------------------------
-- DESCRIPTIONS
SELECT "TABLES";
SHOW tables;
SELECT "Description de la TABLE Disciplines";
DESCRIBE Disciplines;
SELECT * FROM Disciplines;
SELECT "Description de la TABLE des Fonctions du personnel";
DESCRIBE Fonctions;
SELECT * FROM Fonctions;
SELECT "Description de la TABLE du personnel";
DESCRIBE Personnel;
SELECT * FROM Personnel;
SELECT "Description de la TABLE Professeurs";
DESCRIBE Professeurs;
SELECT * FROM Professeurs;

SELECT "UTILISATEURS";
select host, USER, password from mysql.user;


