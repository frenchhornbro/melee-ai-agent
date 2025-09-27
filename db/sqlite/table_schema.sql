PRAGMA foreign_keys = ON;

CREATE TABLE `Player`(
    `id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    `player_tag` VARCHAR(255) NOT NULL UNIQUE,
    `country` VARCHAR(255) NOT NULL
);
CREATE TABLE `Character`(
    `id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE `RankList`(
    `id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    `rank_date` DATE NOT NULL
);
CREATE TABLE `TierList`(
    `id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    `tier_date` DATE NOT NULL
);
CREATE TABLE `PlayerRanking`(
    `player_id` BIGINT UNSIGNED NOT NULL,
    `rank_list_id` BIGINT UNSIGNED NOT NULL,
    `rank` INT NOT NULL,
    PRIMARY KEY(`player_id`, `rank_list_id`),
    FOREIGN KEY(`rank_list_id`) REFERENCES `RankList`(`id`),
    FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`)
);
CREATE TABLE `TierEntry`(
    `character_id` BIGINT UNSIGNED NOT NULL,
    `list_id` BIGINT UNSIGNED NOT NULL,
    `rank` TINYINT NOT NULL,
    `tier` VARCHAR(255) NULL,
    PRIMARY KEY(`character_id`, `list_id`),
    FOREIGN KEY(`list_id`) REFERENCES `TierList`(`id`),
    FOREIGN KEY(`character_id`) REFERENCES `Character`(`id`)
);
CREATE TABLE `Main`(
    `player_id` BIGINT UNSIGNED NOT NULL,
    `character_id` BIGINT UNSIGNED NOT NULL,
    `rank_list_id` BIGINT UNSIGNED NOT NULL,
    PRIMARY KEY(`player_id`, `character_id`, `rank_list_id`),
    FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`),
    FOREIGN KEY(`character_id`) REFERENCES `Character`(`id`),
    FOREIGN KEY(`rank_list_id`) REFERENCES `RankList`(`id`)
);