-- ------------------------------------------------
-- Pour exécuter le script sql d'initialisation
-- À partir du Terminal se rendre dans le dossier où se trouve le script
-- Se connecter en tant que root à mysql avec
-- mysql -u root -p
-- Dans l'invite de commande MariaDB> entrer:
-- SOURCE ./initdb_gestiondesnotes.sql;
-- puis: CALL initialiser;



-- ------------------------------------------------
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+01:00";

-- ------------------------------------------------
-- Création de la base de données
-- Efface l'ancienne bd si elle existait
-- et en crée une nouvelle
SET FOREIGN_KEY_CHECKS=0;
CREATE OR REPLACE DATABASE bd_gestion_des_notes;
USE bd_gestion_des_notes;
SET FOREIGN_KEY_CHECKS=1; -- to re-enable them

-- ------------------------------------------------
-- Création de différents rôles
CREATE OR replace ROLE role_gestionnaire;
GRANT ALL ON bd_gestion_des_notes.* TO role_gestionnaire;
grant ALL PRIVILEGES ON *.* to role_gestionnaire;
FLUSH PRIVILEGES; 

CREATE OR replace ROLE role_professeur;
GRANT SELECT
ON bd_gestion_des_notes.*
TO role_professeur;

-- Si création d'un client élève
-- CREATE ROLE role_eleve;
-- GRANT à définir
-- TO role_eleve;


-- ------------------------------------------------
-- Création de différents utilisateurs avec le rôle de gestionnaire

CREATE OR replace USER  stil@localhost IDENTIFIED BY 's';                 
GRANT role_gestionnaire TO stil@localhost;
SET DEFAULT ROLE role_gestionnaire FOR stil@localhost;
GRANT ALL ON *.* TO stil@localhost WITH GRANT OPTION; 

CREATE OR replace USER  proviseur@localhost IDENTIFIED BY 'p';                 
GRANT role_gestionnaire TO proviseur@localhost;
SET DEFAULT ROLE role_gestionnaire FOR proviseur@localhost;
GRANT ALL ON *.* TO proviseur@localhost WITH GRANT OPTION; 

CREATE OR replace USER  noel_gest@localhost IDENTIFIED BY 'noel';                 
GRANT role_gestionnaire TO noel_gest@localhost;
SET DEFAULT ROLE role_gestionnaire FOR noel_gest@localhost;
GRANT ALL ON *.* TO noel_gest@localhost WITH GRANT OPTION; 

FLUSH PRIVILEGES; 


-- ------------------------------------------------
-- Création de la table des fonctions
-- des gestionnaires de la base de données
CREATE TABLE IF NOT EXISTS Fonction(
Func_Id varchar(10) COLLATE utf8_bin NOT NULL,
Func_Name varchar(30) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (Func_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Fonction (Func_Id, Func_Name) VALUES
('P1', 'Proviseur'),
('P2', 'Proviseur-adjoint'),
('S', 'Secrétaire de direction'),
('ST', 'STIL'),
('DIU', 'Professeur DIU');

show warnings;
-- ------------------------------------------------
-- Création de la table Administrateur
CREATE TABLE IF NOT EXISTS Administrateur(
Admin_Id int NOT NULL AUTO_INCREMENT,
FirstName varchar(30) COLLATE utf8_bin DEFAULT NULL,
LastName varchar(30) COLLATE utf8_bin DEFAULT NULL,
Func_Id varchar(5) COLLATE utf8_bin NOT NULL,
Gender char DEFAULT NULL,
Birthday DATE,
Login varchar(30) COLLATE utf8_bin DEFAULT NULL,
PRIMARY KEY (Admin_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Administrateur(FirstName, LastName, Func_Id, Gender, Birthday, Login) VALUES
('Prénom', 'Nom', 'P1', 'M', '1966-04-20',  'proviseur'),
('Noël', 'Novelli', 'DIU', 'M', '2020-08-25',  'noel_gest'),
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

-- ------------------------------------------------
-- Procédure de création d'utilisateurs avec le rôle de professeur
-- et de remplissage de la table Professeur
-- À exécuter avec: CALL remplir_professeur();

DELIMITER $$  
CREATE PROCEDURE REMPLIR_PROFESSEUR()

   BEGIN
      DECLARE v_a INT Default 1 ;
      DECLARE v_nom VARCHAR(42);
      DECLARE v_prenom VARCHAR(42);
      DECLARE v_login VARCHAR(84);
      DECLARE v_titre VARCHAR(5);
      DECLARE v_pwd VARCHAR(5);
      SET v_pwd = 'p';
      simple_loop: LOOP
         SET v_nom = CONCAT("prof", LPAD(CAST(v_a AS CHAR), 3, '0'));
         SET v_prenom = CONCAT("prenom", LPAD(CAST(v_a AS CHAR), 3, '0'));
         SET v_titre = CASE WHEN RAND() > .5
                  THEN 'M'
                  ELSE 'F' END;
         INSERT INTO Professeur (prenom, nom, titre) VALUES (v_prenom, v_nom, v_titre);
         SET v_login = CONCAT(v_prenom, v_nom);
         SET @sql1 = CONCAT('CREATE OR REPLACE USER ', v_login, '@localhost identified BY  \'p\' ');
         PREPARE stm1 FROM @sql1;
         EXECUTE stm1;
         SET @sql2 = CONCAT('GRANT role_professeur TO ', v_login, '@localhost');
         PREPARE stm2 FROM @sql2;
         EXECUTE stm2;
         SET @sql3 = CONCAT('SET DEFAULT ROLE role_professeur FOR ', v_login, '@localhost');
         PREPARE stm3 FROM @sql3;
         EXECUTE stm3;
         SET v_a=v_a+1;
         IF v_a=51 THEN
            LEAVE simple_loop;
         END IF;
   END LOOP simple_loop;
   DEALLOCATE PREPARE stm1;
   DEALLOCATE PREPARE stm2;
   DEALLOCATE PREPARE stm3;      
END $$

DELIMITER ;

show warnings;

-- ------------------------------------------------
-- Sinon : Exemple de création à la main d'utilisateur avec le rôle de professeur
-- CREATE OR replace USER p@localhost identified BY 'p';
-- GRANT role_professeur TO p@localhost;
-- SET DEFAULT ROLE role_professeur FOR p@localhost;
-- INSERT INTO Professeur (prenom, nom, titre) VALUES ('prof', 'Testeur', 'M');

-- ------------------------------------------------
-- Création de la table Discipline
CREATE or replace TABLE Discipline (
discipline_id int NOT NULL AUTO_INCREMENT,
nom varchar(50) COLLATE utf8_bin NOT NULL,
PRIMARY KEY (discipline_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Discipline (nom) VALUES
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


show warnings;

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

show warnings;

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

show warnings;

-- ------------------------------------------------
-- Création de la table Enseigner
CREATE OR replace TABLE Enseigner (
 professeur_id INT,
 discipline_id INT,
 classe_id INT,
PRIMARY KEY (professeur_id, discipline_id, classe_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exemple:
-- INSERT INTO Enseigner (professeur_id, discipline_id, classe_id) VALUES
-- (1, 2, 3);

-- Remplissage aléatoire de la table Enseigner
-- À exécuter avec: CALL remplir_enseigner(); 


DELIMITER $$  
CREATE PROCEDURE REMPLIR_ENSEIGNER()
   BEGIN
      DECLARE v_professeur INT DEFAULT 1;
      DECLARE v_discipline INT;
      DECLARE v_classe INT;
      simple_loop: LOOP
         SET v_discipline = 1+RAND()*9;
         SET v_classe = 1+RAND()*5; 
         INSERT INTO Enseigner  VALUES (v_professeur, v_discipline, v_classe);
         SET v_classe = 7+RAND()*7; 
         INSERT INTO Enseigner  VALUES (v_professeur, v_discipline, v_classe);
         SET v_professeur=v_professeur+1;
         IF v_professeur=51 THEN
            LEAVE simple_loop;
         END IF;
   END LOOP simple_loop;
END $$

DELIMITER ;

show warnings;

-- ------------------------------------------------
-- Création de la table Evaluation

CREATE OR REPLACE  TABLE Evaluation (
  evaluation_id int NOT NULL AUTO_INCREMENT,
  nom VARCHAR(20) COLLATE utf8_bin NOT NULL,  
  date_controle DATE DEFAULT '2020-10-1',
  date_visible DATE DEFAULT '2020-10-11',
  discipline_id INT,
  professeur_id INT,
  classe_id INT,
  periode_id INT,
  PRIMARY KEY (evaluation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exemple:
-- INSERT INTO Evaluation (date_controle, date_visible, discipline_id, professeur_id, classe_id, periode_id)  VALUES ('C1', 2020-10-5', '2020-10-12', 2, 2, 3, 1);


-- Remplissage aléatoire de la table Evaluation
-- À exécuter avec: CALL remplir_evaluation();

DELIMITER $$  
CREATE PROCEDURE REMPLIR_EVALUATION()
BEGIN
  DECLARE done INT DEFAULT FALSE;
  DECLARE v_nom VARCHAR(20);
  DECLARE v_a INT DEFAULT 1;
  DECLARE v_professeur INT;
  DECLARE v_discipline INT;
  DECLARE v_classe INT;
  DECLARE cur1 CURSOR FOR SELECT professeur_id, discipline_id, classe_id FROM Enseigner;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
  OPEN cur1;
  read_loop: LOOP
    FETCH cur1 INTO v_professeur, v_discipline, v_classe;
    IF done THEN
      LEAVE read_loop;
    END IF;
    SET v_nom=CONCAT('C',CAST(v_a AS CHAR));
    INSERT INTO Evaluation (nom, discipline_id, professeur_id, classe_id, periode_id) VALUES (v_nom, v_discipline, v_professeur, v_classe, 1);
    INSERT INTO Evaluation (nom, discipline_id, professeur_id, classe_id, periode_id) VALUES (v_nom, v_discipline, v_professeur, v_classe, 2);
    INSERT INTO Evaluation (nom, discipline_id, professeur_id, classe_id, periode_id) VALUES (v_nom, v_discipline, v_professeur, v_classe, 3);
    SET v_a=v_a+1;
  END LOOP;
  CLOSE cur1;

END $$

DELIMITER ;


show warnings;


GRANT INSERT, UPDATE, DELETE
ON bd_gestion_des_notes.Evaluation
TO role_professeur;

-- ------------------------------------------------
-- Création de la table Evaluer

CREATE OR REPLACE TABLE Evaluer (
  evaluation_id INT,
  eleve_id INT,
  note DECIMAL(4, 2), 
  PRIMARY KEY (evaluation_id, eleve_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Exemple:
-- INSERT INTO Evaluer (evaluation_id, eleve_id, note)  VALUES (2, 2, 17);

GRANT INSERT, UPDATE, DELETE
ON bd_gestion_des_notes.Evaluer
TO role_professeur;



-- ------------------------------------------------
-- Clés étrangères

ALTER TABLE Eleve ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);
ALTER TABLE Enseigner ADD FOREIGN KEY (discipline_id) REFERENCES Discipline (discipline_id);
ALTER TABLE Enseigner ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);
ALTER TABLE Enseigner ADD FOREIGN KEY (professeur_id) REFERENCES Professeur (professeur_id);
ALTER TABLE Evaluation ADD FOREIGN KEY (periode_id) REFERENCES Periode (periode_id);
ALTER TABLE Evaluation ADD FOREIGN KEY (classe_id) REFERENCES Classe (classe_id);
ALTER TABLE Evaluation ADD FOREIGN KEY (professeur_id) REFERENCES Professeur (professeur_id);
ALTER TABLE Evaluation ADD FOREIGN KEY (discipline_id) REFERENCES Discipline (discipline_id);
ALTER TABLE Classe ADD FOREIGN KEY (annee_id) REFERENCES Anneescolaire (annee_id);
ALTER TABLE Evaluer ADD FOREIGN KEY (eleve_id) REFERENCES Eleve (eleve_id);
ALTER TABLE Evaluer ADD FOREIGN KEY (evaluation_id) REFERENCES Evaluation (evaluation_id);




-- ------------------------------------------------
-- DESCRIPTIONS DES TABLES
SHOW tables;
SELECT "Description de la TABLE Discipline";
DESCRIBE Discipline;
SELECT "Description de la TABLE des Fonctions du personnel";
DESCRIBE Fonction;
SELECT "Description de la TABLE Administrateur";
DESCRIBE Administrateur;
SELECT "Description de la TABLE Professeur";
DESCRIBE Professeur;
SELECT "Description de la TABLE Eleve";
DESCRIBE Eleve;
SELECT "Description de la TABLE Classe";
DESCRIBE Classe;
SELECT "Description de la TABLE Periode";
DESCRIBE Periode;
SELECT "Description de la TABLE Anneescolaire";
DESCRIBE Anneescolaire;
SELECT "Description de la TABLE Enseigner";
DESCRIBE Enseigner;
SELECT "Description de la TABLE Evaluation";
DESCRIBE Evaluation;
SELECT "Description de la TABLE Evaluer";
DESCRIBE Evaluer;

-- ------------------------------------------------
-- Procédure d'initialisation globale qui appelle
-- les autres procédures d'initialisation dans l'ordre souhaité

DELIMITER $$  
CREATE PROCEDURE INITIALISER()

   BEGIN
      CALL remplir_professeur();
      CALL remplir_enseigner();
      CALL remplir_evaluation();
      
      SELECT * FROM Discipline;
      SELECT * FROM Fonction;
      SELECT * FROM Administrateur;
      SELECT * FROM Professeur;
      SELECT * FROM Eleve;
      SELECT * FROM Classe;
      SELECT * FROM Periode;
      SELECT * FROM Anneescolaire;
      SELECT * FROM Enseigner;
      SELECT * FROM Evaluation;
      SELECT * FROM Evaluer;      

      SELECT "UTILISATEURS";
      select host, USER, password from mysql.USER;
      
END $$

DELIMITER ;

show warnings;


