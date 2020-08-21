CREATE DATABASE IF NOT EXISTS `MOCODO_GESTION_NOTES` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `MOCODO_GESTION_NOTES`;

CREATE TABLE `DISCIPLINE` (
  `discipline_id` VARCHAR(42),
  `nom` VARCHAR(42),
  PRIMARY KEY (`discipline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ENSEIGNER` (
  `professeur_id` VARCHAR(42),
  `classe_id` VARCHAR(42),
  `discipline_id` VARCHAR(42),
  PRIMARY KEY (`professeur_id`, `classe_id`, `discipline_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `PROFESSEUR` (
  `professeur_id` VARCHAR(42),
  `prenom` VARCHAR(42),
  `nom` VARCHAR(42),
  `titre` VARCHAR(42),
  PRIMARY KEY (`professeur_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `EVALUATION` (
  `evaluation_id` VARCHAR(42),
  `date_contrôle` VARCHAR(42),
  `date_note_visible` VARCHAR(42),
  `discipline_id` VARCHAR(42),
  `professeur_id` VARCHAR(42),
  `classe_id` VARCHAR(42),
  `annee_id` VARCHAR(42),
  `periode_id` VARCHAR(42),
  PRIMARY KEY (`evaluation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `CLASSE` (
  `classe_id` VARCHAR(42),
  `nom` VARCHAR(42),
  `niveau` VARCHAR(42),
  `annee_id` VARCHAR(42),
  PRIMARY KEY (`classe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `EVALUER` (
  `evaluation_id` VARCHAR(42),
  `eleve_id` VARCHAR(42),
  `note` VARCHAR(42),
  PRIMARY KEY (`evaluation_id`, `eleve_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ELEVE` (
  `eleve_id` VARCHAR(42),
  `prénom` VARCHAR(42),
  `nom` VARCHAR(42),
  `genre` VARCHAR(42),
  `classe_id` VARCHAR(42),
  PRIMARY KEY (`eleve_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `PERIODE` (
  `periode_id` VARCHAR(42),
  `nom` VARCHAR(42),
  PRIMARY KEY (`periode_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `ANNEESCOLAIRE` (
  `annee_id` VARCHAR(42),
  `nom` VARCHAR(42),
  PRIMARY KEY (`annee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

ALTER TABLE `ENSEIGNER` ADD FOREIGN KEY (`discipline_id`) REFERENCES `DISCIPLINE` (`discipline_id`);
ALTER TABLE `ENSEIGNER` ADD FOREIGN KEY (`classe_id`) REFERENCES `CLASSE` (`classe_id`);
ALTER TABLE `ENSEIGNER` ADD FOREIGN KEY (`professeur_id`) REFERENCES `PROFESSEUR` (`professeur_id`);
ALTER TABLE `EVALUATION` ADD FOREIGN KEY (`periode_id`) REFERENCES `PERIODE` (`periode_id`);
ALTER TABLE `EVALUATION` ADD FOREIGN KEY (`annee_id`) REFERENCES `ANNEESCOLAIRE` (`annee_id`);
ALTER TABLE `EVALUATION` ADD FOREIGN KEY (`classe_id`) REFERENCES `CLASSE` (`classe_id`);
ALTER TABLE `EVALUATION` ADD FOREIGN KEY (`professeur_id`) REFERENCES `PROFESSEUR` (`professeur_id`);
ALTER TABLE `EVALUATION` ADD FOREIGN KEY (`discipline_id`) REFERENCES `DISCIPLINE` (`discipline_id`);
ALTER TABLE `CLASSE` ADD FOREIGN KEY (`annee_id`) REFERENCES `ANNEESCOLAIRE` (`annee_id`);
ALTER TABLE `EVALUER` ADD FOREIGN KEY (`eleve_id`) REFERENCES `ELEVE` (`eleve_id`);
ALTER TABLE `EVALUER` ADD FOREIGN KEY (`evaluation_id`) REFERENCES `EVALUATION` (`evaluation_id`);
ALTER TABLE `ELEVE` ADD FOREIGN KEY (`classe_id`) REFERENCES `CLASSE` (`classe_id`);