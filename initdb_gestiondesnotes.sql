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
('Kunihiko', 'Kodaira', 1, 'M'),
('Pierre', 'Serre', 2, 'M'),
('Klaus', 'Roth', 3, 'M'),
('René', 'Thom', 4, 'M'),
('Lars', 'Hörmander', 1, 'M'),
('John', 'Milnor', 2, 'M'),
('Michael', 'Atiyah', 3, 'M'),
('Paul', 'Cohen', 4, 'M'),
('Alexandre', 'Grothendieckd', 1, 'M'),
('Stephen', 'Smale', 2, 'M'),
('Alan', 'Baker', 3, 'M'),
('Heisuke', 'Hironaka', 4, 'M'),
('Sergueï', 'Novikov', 1, 'M'),
('Griggs', 'Thompson', 2, 'M'),
('Enrico', 'Bombieri', 3, 'M'),
('David', 'Mumford', 4, 'M'),
('Pierre', 'Deligne', 1, 'M'),
('Charles', 'Fefferman', 2, 'M'),
('Gregori', 'Margulis', 3, 'M'),
('Daniel', 'Quillen', 4, 'M'),
('Alain', 'Connes', 1, 'M'),
('William', 'Thurston', 2, 'M'),
('Tung', 'Yaue', 3, 'M'),
('Simon', 'Donaldson', 4, 'M'),
('Gerd', 'Faltings', 1, 'M'),
('Michael', 'Freedman', 2, 'M'),
('Vladimir', 'Drinfeld', 3, 'M'),
('Vaughan', 'Jones', 4, 'M'),
('Shigefumi', 'Mori', 1, 'M'),
('Edward', 'Witten', 2, 'M'),
('Jean', 'Bourgain', 3, 'M'),
('Louis', 'Lions', 4, 'M'),
('Christophe', 'Yoccoz', 1, 'M'),
('Efim', 'Zelmanov', 2, 'M'),
('Ewen', 'Borcherds', 3, 'M'),
('Timothy', 'Gowers', 4, 'M'),
('Maxim', 'Kontsevich', 1, 'M'),
('Curtis', 'McMullen', 2, 'M'),
('Laurent', 'Lafforgue', 3, 'M'),
('Vladimir', 'Voevodsky', 4, 'M'),
('Andreï', 'Okounkov', 1, 'M'),
('Terence', 'Tao', 2, 'M'),
('Wendelin', 'Werner', 3, 'M'),
('Elon', 'Lindenstrauss', 4, 'M'),
('Bảo', 'Châu', 1, 'M'),
('Stanislav', 'Smirnov', 2, 'M'),
('Cédric', 'Villani', 3, 'M'),
('Artur', 'Ávila', 4, 'M'),
('Manjul', 'Bhargava', 1, 'M'),
('Martin', 'Hairer', 2, 'M'),
('Maryam', 'Mirzakhani', 3, 'F'),
('Caucher', 'Birkar', 4, 'M'),
('Alessio', 'Figalli', 1, 'M'),
('Peter', 'Scholze', 2, 'M'),
('Akshay', 'Venkatesh', 3, 'M'),
('Marie', 'Curie', 1, 'F'),
('Irène', 'Joliot-Curie', 2, 'F'),
('Gerty', 'Cori', 3, 'F'),
('Maria', 'Goeppert-Mayer', 4, 'F'),
('Dorothy', 'Crowfoot-Hodgkin', 1, 'F'),
('Rosalyn', 'Yalow', 2, 'F'),
('Barbara', 'McClintock', 3, 'F'),
('Rita', 'Levi-Montalcini', 4, 'F'),
('Gertrude', 'Elion', 1, 'F'),
('Christiane', 'Nüsslein-Volhard', 2, 'F'),
('Linda', 'Buck', 3, 'F'),
('Françoise', 'Barré-Sinoussi', 4, 'F'),
('Elizabeth', 'Blackburn', 1, 'F'),
('Carol', 'Greider', 2, 'F'),
('Ada', 'Yonath', 3, 'F'),
('May-Britt', 'Moser', 4, 'F'),
('Youyou', 'Tu', 1, 'F');



-- ------------------------------------------------
-- Création de la table disciplines
CREATE or replace TABLE Disciplines (
Disc_Id int NOT NULL AUTO_INCREMENT,
Disc_Name varchar(20) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (Disc_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Disciplines (Disc_Name) VALUES
('FRANÇAIS'),
('MATHÉMATIQUES'),
('NSI'),
('PHYSIQUE-CHIMIE');


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


