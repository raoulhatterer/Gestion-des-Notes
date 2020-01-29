SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS Professeurs (
    Prof_Id int NOT NULL AUTO_INCREMENT,
    LastName varchar(20) COLLATE utf8_bin NOT NULL,
    FirstName varchar(20) COLLATE utf8_bin NOT NULL,
    Disc_Id int,
    Birthday date,
    Grade varchar(20) COLLATE utf8_bin DEFAULT NULL,
    Password varchar(20) COLLATE utf8_bin DEFAULT NULL,
    PRIMARY KEY (Prof_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Professeurs (LastName, FirstName, Disc_Id) VALUES
   ('Kidman', 'Nicole', 1),
   ('Bettany', 'Paul', 1),
   ('Glen', 'John', 2);

-- ------------------------------------------------
CREATE TABLE IF NOT EXISTS Disciplines (
    Disc_Id int(10),
    Disc_Name varchar(20) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (Disc_Id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO Disciplines (Disc_Id, Disc_Name) VALUES
    (1, 'mathématiques'),
    (2, 'physique-chimie'),
    (3, 'français'),
    (4, 'NSI');
