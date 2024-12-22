CREATE TABLE `genres` (
    `id` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    PRIMARY KEY(`id`)
);

CREATE TABLE `language` (
    `id` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(64),
    PRIMARY KEY(`id`)
);

CREATE TABLE `series` (  -- Renamed for consistency
    `id` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `description` TEXT,
    `note` TEXT,  -- Renamed for consistency
    PRIMARY KEY(`id`)
);

CREATE TABLE `publisher` (
    `id` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `description` TEXT,
    `note` TEXT,  -- Renamed for consistency
    `webpage` TEXT,
    PRIMARY KEY(`id`)
);

CREATE TABLE `Authors` (
    `id` INT NOT NULL AUTO_INCREMENT UNIQUE,
    `name` VARCHAR(255),
    `nationality_id` INT PRIMARY KEY,
    FOREIGN KEY (`nationality_id`) REFERENCES language(id) ON DELETE CASCADE,
    `description` TEXT,
    `birth_date` DATE,  -- Renamed for consistency
    `death_date` DATE,  -- Renamed for consistency
    `note` TEXT,  -- Renamed for consistency
    PRIMARY KEY(`id`)
);

CREATE TABLE `Books` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `isbn` VARCHAR(13),
    `title` VARCHAR(512) NOT NULL,
    `genre_id` INT PRIMARY KEY,
    FOREIGN KEY (`genre_id`) REFERENCES genres(id) ON DELETE CASCADE,
    `release_date` DATE,  -- Renamed for consistency
    `first_polish_release_date` DATE,  -- Renamed for consistency
    `format` ENUM('unknown', 'hardback', 'paperback', 'ebook') NOT NULL DEFAULT 'unknown',
    `language_id` INT PRIMARY KEY,
    FOREIGN KEY (`language_id`) REFERENCES language(id) ON DELETE CASCADE,
    `pages` INT,
    `description` TEXT,
    `note` TEXT,  -- Renamed for consistency
    `series_id` INT PRIMARY KEY,
    FOREIGN KEY (`series_id`) REFERENCES series(id) ON DELETE CASCADE,
    `original_title` VARCHAR(512),  -- Renamed for consistency
    `translator` VARCHAR(512),
    `publisher_id` INT PRIMARY KEY,
    FOREIGN KEY (`publisher_id`) REFERENCES publisher(id) ON DELETE CASCADE
);


CREATE TABLE `bookAuthors` (
    `book_id` INT,
    `author_id` INT,
    PRIMARY KEY (`book_id`, `author_id`),
    FOREIGN KEY (`book_id`) REFERENCES Books(`id`) ON DELETE CASCADE,  -- Corrected reference to id
    FOREIGN KEY (`author_id`) REFERENCES Authors(`id`) ON DELETE CASCADE  -- Corrected reference to id
);
