-- The fork's DBCStores.cpp loads DB overrides for CharSections.dbc and EmotesTextSound.dbc, but the
-- tables were only ever created by mod-playerbots' world SQL, so a tree without that module aborted at
-- startup. Core owns the dependency, so core creates the tables. IF NOT EXISTS leaves any copy a module
-- already created untouched. Both are schema-only: rows are optional overrides of the client DBC data.
CREATE TABLE IF NOT EXISTS `charsections_dbc` (
  `Id` INT NOT NULL DEFAULT '0',
  `Race` INT NOT NULL DEFAULT '0',
  `Gender` INT NOT NULL DEFAULT '0',
  `GenType` INT NOT NULL DEFAULT '0',
  `TexturePath1` VARCHAR(100) DEFAULT NULL,
  `TexturePath2` VARCHAR(100) DEFAULT NULL,
  `TexturePath3` VARCHAR(100) DEFAULT NULL,
  `Flags` INT NOT NULL DEFAULT '0',
  `Type` INT NOT NULL DEFAULT '0',
  `Color` INT NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `emotetextsound_dbc` (
  `Id` INT NOT NULL DEFAULT '0',
  `EmotesTextId` INT NOT NULL DEFAULT '0',
  `RaceId` INT NOT NULL DEFAULT '0',
  `SexId` INT NOT NULL DEFAULT '0',
  `SoundId` INT NOT NULL DEFAULT '0',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
