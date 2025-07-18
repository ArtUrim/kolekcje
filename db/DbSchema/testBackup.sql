-- Adminer 4.8.1 MySQL 11.5.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `katalog`;
CREATE DATABASE `katalog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `katalog`;

DROP TABLE IF EXISTS `Authors`;
CREATE TABLE `Authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `nationality_id` char(3) NOT NULL,
  `description` text DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `death_date` date DEFAULT NULL,
  `note` text DEFAULT NULL,
  PRIMARY KEY (`id`,`nationality_id`),
  UNIQUE KEY `id` (`id`),
  KEY `nationality_id` (`nationality_id`),
  CONSTRAINT `Authors_ibfk_1` FOREIGN KEY (`nationality_id`) REFERENCES `language` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `Authors`;
INSERT INTO `Authors` (`id`, `name`, `nationality_id`, `description`, `birth_date`, `death_date`, `note`) VALUES
(1,	'Ewa Bosek',	'pl_',	NULL,	NULL,	NULL,	NULL),
(2,	'Paweł Pompa',	'pl_',	NULL,	NULL,	NULL,	NULL),
(3,	'Aleks Dybka',	'pl_',	NULL,	NULL,	NULL,	NULL),
(4,	'Olaf Chaba',	'pl_',	NULL,	NULL,	NULL,	NULL),
(5,	'Nicole Szpila',	'pl_',	NULL,	NULL,	NULL,	NULL),
(6,	'Kornelia Migoń',	'pl_',	NULL,	NULL,	NULL,	NULL),
(7,	'Kazimierz Wojsław',	'pl_',	NULL,	NULL,	NULL,	NULL),
(8,	'Witold Słabosz',	'pl_',	NULL,	NULL,	NULL,	NULL),
(9,	'Aurelia Brzykcy',	'pl_',	NULL,	NULL,	NULL,	NULL),
(10,	'Kazimierz Pęciak',	'pl_',	NULL,	NULL,	NULL,	NULL),
(11,	'Ewelina Małys',	'pl_',	NULL,	NULL,	NULL,	NULL),
(12,	'Adrianna Skoneczna',	'pl_',	NULL,	NULL,	NULL,	NULL);

DROP TABLE IF EXISTS `bookAuthors`;
CREATE TABLE `bookAuthors` (
  `book_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `bookAuthors_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookAuthors_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `Authors` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `bookAuthors`;
INSERT INTO `bookAuthors` (`book_id`, `author_id`) VALUES
(11,	1),
(1,	2),
(2,	2),
(6,	2),
(7,	2),
(15,	2),
(20,	2),
(12,	3),
(15,	3),
(18,	3),
(16,	4),
(17,	4),
(3,	5),
(8,	6),
(14,	6),
(18,	6),
(19,	6),
(13,	7),
(19,	7),
(20,	7),
(14,	9),
(19,	9),
(10,	10),
(17,	10),
(20,	10),
(4,	11),
(5,	11),
(9,	11),
(16,	11),
(13,	12);

DROP TABLE IF EXISTS `bookGenres`;
CREATE TABLE `bookGenres` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `bookGenres_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookGenres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `bookGenres`;
INSERT INTO `bookGenres` (`book_id`, `genre_id`) VALUES
(13,	1),
(8,	2),
(12,	2),
(16,	2),
(19,	2),
(4,	3),
(5,	3),
(6,	3),
(6,	4),
(8,	4),
(17,	4),
(3,	5),
(17,	5),
(9,	6),
(14,	6),
(18,	6),
(6,	7),
(9,	7),
(15,	7),
(17,	7),
(20,	7),
(1,	8),
(2,	8),
(3,	8),
(5,	8),
(7,	8),
(9,	8),
(2,	9),
(10,	9),
(13,	9),
(1,	10),
(2,	10),
(8,	10),
(19,	10),
(3,	11),
(19,	11),
(10,	12),
(11,	12),
(12,	12),
(13,	12);

DROP TABLE IF EXISTS `bookPublishers`;
CREATE TABLE `bookPublishers` (
  `book_id` int(11) NOT NULL,
  `publisher_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`publisher_id`),
  KEY `publisher_id` (`publisher_id`),
  CONSTRAINT `bookPublishers_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookPublishers_ibfk_2` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `bookPublishers`;
INSERT INTO `bookPublishers` (`book_id`, `publisher_id`) VALUES
(2,	1),
(8,	2),
(18,	2),
(12,	3),
(20,	3),
(3,	4),
(6,	4),
(7,	4),
(9,	4),
(13,	4),
(17,	4),
(1,	5),
(4,	5),
(5,	5),
(14,	5),
(19,	5),
(10,	6),
(11,	6),
(15,	6),
(16,	6);

DROP TABLE IF EXISTS `Books`;
CREATE TABLE `Books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(13) DEFAULT NULL,
  `title` varchar(512) NOT NULL,
  `release_date` year(4) DEFAULT NULL,
  `first_polish_release_date` year(4) DEFAULT NULL,
  `format` enum('unknown','hardback','paperback','ebook') NOT NULL DEFAULT 'unknown',
  `pages` int(11) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `note` text DEFAULT NULL,
  `series_id` int(11) DEFAULT NULL,
  `original_title` varchar(512) DEFAULT NULL,
  `translator` varchar(512) DEFAULT NULL,
  `language_id` char(3) NOT NULL,
  PRIMARY KEY (`id`,`language_id`),
  KEY `language_id` (`language_id`),
  KEY `series_id` (`series_id`),
  CONSTRAINT `Books_ibfk_2` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `Books_ibfk_3` FOREIGN KEY (`series_id`) REFERENCES `series` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `Books`;
INSERT INTO `Books` (`id`, `isbn`, `title`, `release_date`, `first_polish_release_date`, `format`, `pages`, `description`, `note`, `series_id`, `original_title`, `translator`, `language_id`) VALUES
(1,	'6155849576385',	'Mocz powodować orzeł niż',	'2022',	'2022',	'hardback',	298,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(2,	'0238314958802',	'Podawać życie',	'1979',	'1979',	'paperback',	121,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(3,	'5140786859140',	'Godność',	'1980',	'1980',	'paperback',	193,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(4,	'2364278688288',	'Termin żywy',	'1977',	'1977',	'unknown',	116,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(5,	'7012310623462',	'Czasami panna',	'1967',	'1967',	'paperback',	223,	NULL,	NULL,	NULL,	NULL,	NULL,	'pl_'),
(6,	'4134187656765',	'Wydać ptak pogląd',	'1964',	'1964',	'ebook',	202,	NULL,	NULL,	NULL,	NULL,	NULL,	'pl_'),
(7,	'3035728008895',	'Byk warstwa królewski dlatego',	'1976',	'1976',	'paperback',	101,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(8,	'4971463793014',	'Niż żeński',	'1987',	'1987',	'unknown',	315,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(9,	'0101779120400',	'Policja literatura',	'1979',	'1979',	'paperback',	110,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(10,	'7874168182695',	'Zazwyczaj milion',	'1994',	'1994',	'ebook',	269,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(11,	'4694088460791',	'Czynność panować minuta intensywny',	'2002',	'2002',	'hardback',	132,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(12,	'7528483159893',	'Zachowywać Się',	'1972',	'1972',	'ebook',	310,	NULL,	NULL,	NULL,	NULL,	NULL,	'pl_'),
(13,	'8051448433020',	'Robak wczoraj',	'2010',	'2010',	'unknown',	314,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(14,	'8369143069005',	'Plecy poprzez',	'2021',	'2021',	'hardback',	262,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(15,	'5525643145120',	'Lata traktować',	'1996',	'1996',	'ebook',	201,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(16,	'3335021703829',	'Osiem korzystać teren',	'1963',	'1963',	'paperback',	217,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(17,	'6016021440502',	'Móc tutaj piętnaście',	'1990',	'1990',	'hardback',	158,	NULL,	NULL,	1,	NULL,	NULL,	'pl_'),
(18,	'6998785195178',	'Uczyć Się jądro',	'1977',	'1977',	'ebook',	236,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(19,	'8677726967588',	'Postępowanie łąka żydowski',	'2003',	'2003',	'paperback',	124,	NULL,	NULL,	2,	NULL,	NULL,	'pl_'),
(20,	'2430336570582',	'Odnosić Się poniedziałek czerwony wstyd',	'1961',	'1961',	'hardback',	305,	NULL,	NULL,	1,	NULL,	NULL,	'pl_');

DROP TABLE IF EXISTS `genres`;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `genres`;
INSERT INTO `genres` (`id`, `name`) VALUES
(1,	'poradnik'),
(2,	'proza'),
(3,	'historia'),
(4,	'komiks'),
(5,	'poezja'),
(6,	'fantastyka'),
(7,	'sztuka'),
(8,	'orientalia'),
(9,	'nauka'),
(10,	'języki'),
(11,	'słownik'),
(12,	'humanistyka');

DROP TABLE IF EXISTS `language`;
CREATE TABLE `language` (
  `id` char(3) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `language`;
INSERT INTO `language` (`id`, `name`) VALUES
('en_',	'angielski'),
('arm',  'ormiański'),
('it_',	'włoski'),
('kr_',	'koreański'),
('pl_',	'polski');

DROP TABLE IF EXISTS `publisher`;
CREATE TABLE `publisher` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `note` text DEFAULT NULL,
  `webpage` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `publisher`;
INSERT INTO `publisher` (`id`, `name`, `description`, `note`, `webpage`) VALUES
(1,	'dialogi',	NULL,	NULL,	NULL),
(2,	'monologi',	NULL,	NULL,	NULL),
(3,	'katalogi',	NULL,	NULL,	NULL),
(4,	'diatryby',	NULL,	NULL,	NULL),
(5,	'inne tryby',	NULL,	NULL,	NULL),
(6,	'po prostu',	NULL,	NULL,	NULL);

DROP TABLE IF EXISTS `series`;
CREATE TABLE `series` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `note` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

TRUNCATE `series`;
INSERT INTO `series` (`id`, `name`, `description`, `note`) VALUES
(1,	'paczki',	NULL,	NULL),
(2,	'kłaczki',	NULL,	NULL);

-- 2025-07-18 14:12:33
