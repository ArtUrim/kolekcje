-- Adminer 4.8.1 MySQL 11.6.2-MariaDB-ubu2404 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

CREATE DATABASE `katalog` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_uca1400_ai_ci */;
USE `katalog`;

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


CREATE TABLE `bookAuthors` (
  `book_id` int(11) NOT NULL,
  `author_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `bookAuthors_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookAuthors_ibfk_2` FOREIGN KEY (`author_id`) REFERENCES `Authors` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `bookGenres` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `genre_id` (`genre_id`),
  CONSTRAINT `bookGenres_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookGenres_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `bookPublishers` (
  `book_id` int(11) NOT NULL,
  `publisher_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`publisher_id`),
  KEY `publisher_id` (`publisher_id`),
  CONSTRAINT `bookPublishers_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `Books` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION,
  CONSTRAINT `bookPublishers_ibfk_2` FOREIGN KEY (`publisher_id`) REFERENCES `publisher` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


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


CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


CREATE TABLE `language` (
  `id` char(3) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


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


CREATE TABLE `series` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `note` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;


-- 2025-01-14 16:17:09
