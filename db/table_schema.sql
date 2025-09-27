CREATE TABLE `Player`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `player_tag` VARCHAR(255) NOT NULL UNIQUE,
    `country` VARCHAR(255) NOT NULL
);
CREATE TABLE `PlayerRanking`(
    `player_id` BIGINT UNSIGNED NOT NULL,
    `rank_list_id` BIGINT NOT NULL,
    `rank` INT NOT NULL,
    PRIMARY KEY(`player_id`, `rank_list_id`),
    CONSTRAINT `playerranking_rank_list_id_foreign` FOREIGN KEY(`rank_list_id`) REFERENCES `RankList`(`id`),
    CONSTRAINT `playerranking_player_id_foreign` FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`)
);
CREATE TABLE `Character`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE `TierEntry`(
    `character_id` BIGINT NOT NULL,
    `list_id` BIGINT NOT NULL,
    `rank` TINYINT NOT NULL,
    `tier` VARCHAR(255) NULL,
    PRIMARY KEY(`character_id`, `list_id`),
    CONSTRAINT `tierentry_list_id_foreign` FOREIGN KEY(`list_id`) REFERENCES `TierList`(`id`),
    CONSTRAINT `tierentry_character_id_foreign` FOREIGN KEY(`character_id`) REFERENCES `Character`(`id`)
);
CREATE TABLE `RankList`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `rank_date` DATE NOT NULL
);
CREATE TABLE `Main`(
    `player_id` BIGINT UNSIGNED NOT NULL,
    `character_id` BIGINT NOT NULL,
    `rank_list_id` BIGINT NOT NULL,
    PRIMARY KEY(`player_id`, `character_id`, `rank_list_id`),
    CONSTRAINT `main_player_id_foreign` FOREIGN KEY(`player_id`) REFERENCES `Player`(`id`),
    CONSTRAINT `main_character_id_foreign` FOREIGN KEY(`character_id`) REFERENCES `Character`(`id`),
    CONSTRAINT `main_rank_list_id_foreign` FOREIGN KEY(`rank_list_id`) REFERENCES `RankList`(`id`)
);
CREATE TABLE `TierList`(
    `id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `tier_date` DATE NOT NULL
);