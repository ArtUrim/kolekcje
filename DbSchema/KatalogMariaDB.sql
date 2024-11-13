CREATE OR REPLACE TABLE `genres` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(255),
	PRIMARY KEY(`id`)
);

CREATE OR REPLACE TABLE `language` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(64),
	PRIMARY KEY(`id`)
);

CREATE OR REPLACE TABLE `series` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(255),
	`description` TEXT,
	`note` TEXT,
	PRIMARY KEY(`id`)
);

CREATE OR REPLACE TABLE `publisher` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(255),
	`description` TEXT,
	`note` TEXT,
	`webpage` TEXT,
	PRIMARY KEY(`id`)
);

CREATE OR REPLACE TABLE `Authors` (
	`id` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` VARCHAR(255),
	`nationality_id` INT,
	`description` TEXT,
	`birth_date` DATE,
	`death_date` DATE,
	`note` TEXT,
	PRIMARY KEY(`id`, `nationality_id`)
);

CREATE OR REPLACE TABLE `Books` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`isbn` VARCHAR(13),
	`title` VARCHAR(512) NOT NULL,
	`genre_id` INT,
	`release_date` DATE,
	`first_polish_release_date` DATE,
	`format` ENUM("unknown", "hardback", "paperback", "ebook") NOT NULL DEFAULT 'unknown',
	`publisher_id` INT,
	`pages` INT,
	`description` TEXT,
	`note` TEXT,
	`series_id` INT,
	`original_title` VARCHAR(512),
	`translator` VARCHAR(512),
	`language_id` INT,
	PRIMARY KEY(`id`, `genre_id`, `publisher_id`, `series_id`, `language_id`)
);

CREATE OR REPLACE TABLE `bookAuthors` (
	`book_id` INT,
	`author_id` INT,
	PRIMARY KEY(`book_id`, `author_id`)
);

ALTER TABLE `Authors`
ADD FOREIGN KEY(`nationality_id`) REFERENCES `language`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `Books`
ADD FOREIGN KEY(`genre_id`) REFERENCES `genres`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `Books`
ADD FOREIGN KEY(`language_id`) REFERENCES `language`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `Books`
ADD FOREIGN KEY(`series_id`) REFERENCES `series`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `Books`
ADD FOREIGN KEY(`publisher_id`) REFERENCES `publisher`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `bookAuthors`
ADD FOREIGN KEY(`book_id`) REFERENCES `Books`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;
ALTER TABLE `bookAuthors`
ADD FOREIGN KEY(`author_id`) REFERENCES `Authors`(`id`)
ON UPDATE NO ACTION ON DELETE CASCADE;