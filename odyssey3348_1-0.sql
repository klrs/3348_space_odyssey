-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.2.12-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for odyssey3348
DROP DATABASE IF EXISTS `odyssey3348`;
CREATE DATABASE IF NOT EXISTS `odyssey3348` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `odyssey3348`;

DROP USER IF EXISTS 'dbuser6'@'localhost';
CREATE USER 'dbuser6'@'localhost' IDENTIFIED BY 'dbpass6';
GRANT SELECT, INSERT, UPDATE, DELETE ON odyssey3348.* TO dbuser6@localhost;

-- Dumping structure for table odyssey3348.ability
CREATE TABLE IF NOT EXISTS `ability` (
  `AbilityId` int(11) NOT NULL,
  `AbilityName` varchar(50) DEFAULT NULL,
  `MaxUseNo` int(11) DEFAULT NULL,
  `AddStr` int(11) DEFAULT NULL,
  `AddPerc` int(11) DEFAULT NULL,
  `AddIntel` int(11) DEFAULT NULL,
  `AddLuck` int(11) DEFAULT NULL,
  PRIMARY KEY (`AbilityId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.ability: ~0 rows (approximately)
/*!40000 ALTER TABLE `ability` DISABLE KEYS */;
/*!40000 ALTER TABLE `ability` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.enemy
CREATE TABLE IF NOT EXISTS `enemy` (
  `EnemyId` int(11) NOT NULL,
  `CurrentHP` float DEFAULT NULL,
  `CurrentStr` int(11) DEFAULT NULL,
  `CurrentPerc` int(11) DEFAULT NULL,
  `CurrentIntel` int(11) DEFAULT NULL,
  `CurrentLuck` int(11) DEFAULT NULL,
  `EnemyTypeId` int(11) NOT NULL,
  `LocationId` int(11) DEFAULT NULL,
  PRIMARY KEY (`EnemyId`),
  KEY `EnemyTypeId` (`EnemyTypeId`),
  KEY `LocationId` (`LocationId`),
  CONSTRAINT `enemy_ibfk_1` FOREIGN KEY (`EnemyTypeId`) REFERENCES `enemytype` (`EnemyTypeId`),
  CONSTRAINT `enemy_ibfk_2` FOREIGN KEY (`LocationId`) REFERENCES `location` (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.enemy: ~31 rows (approximately)
/*!40000 ALTER TABLE `enemy` DISABLE KEYS */;
INSERT INTO `enemy` (`EnemyId`, `CurrentHP`, `CurrentStr`, `CurrentPerc`, `CurrentIntel`, `CurrentLuck`, `EnemyTypeId`, `LocationId`) VALUES
	(1, 50, 3, 4, 1, 3, 2, 112),
	(2, 120, 6, 8, 3, 2, 8, 203),
	(3, 100, 7, 5, 2, 4, 3, 204),
	(4, 100, 7, 5, 2, 4, 3, 207),
	(5, 100, 7, 5, 2, 4, 3, 207),
	(6, 200, 8, 5, 2, 4, 4, 208),
	(7, 50, 3, 4, 1, 3, 2, 209),
	(8, 50, 3, 4, 1, 3, 2, 209),
	(9, 50, 3, 4, 1, 3, 2, 209),
	(10, 400, 10, 8, 8, 5, 6, 210),
	(11, 50, 3, 4, 1, 3, 2, 212),
	(12, 50, 3, 4, 1, 3, 2, 212),
	(13, 50, 3, 4, 1, 3, 2, 212),
	(14, 50, 3, 4, 1, 3, 2, 212),
	(15, 50, 3, 4, 1, 3, 2, 212),
	(16, 50, 3, 4, 1, 3, 2, 212),
	(17, 50, 3, 4, 1, 3, 2, 212),
	(18, 50, 3, 4, 1, 3, 2, 212),
	(19, 50, 3, 4, 1, 3, 2, 212),
	(20, 50, 3, 4, 1, 3, 2, 212),
	(21, 50, 3, 4, 1, 3, 2, 212),
	(22, 50, 3, 4, 1, 3, 2, 212),
	(23, 50, 3, 4, 1, 3, 2, 212),
	(24, 50, 3, 4, 1, 3, 2, 212),
	(25, 50, 3, 4, 1, 3, 2, 212),
	(26, 50, 3, 4, 1, 3, 2, 212),
	(27, 300, 9, 7, 6, 5, 5, 213),
	(28, 250, 6, 8, 5, 5, 10, 214),
	(29, 1500, 10, 10, 10, 10, 1, NULL),
	(30, 800, 8, 8, 8, 8, 13, NULL),
	(31, 800, 8, 8, 8, 8, 14, NULL);
/*!40000 ALTER TABLE `enemy` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.enemytype
CREATE TABLE IF NOT EXISTS `enemytype` (
  `EnemyTypeId` int(11) NOT NULL,
  `EnemyTypeName` varchar(50) DEFAULT NULL,
  `EnemyTypeDescription` varchar(2000) DEFAULT NULL,
  `MaxHP` float DEFAULT NULL,
  `MaxStr` int(11) DEFAULT NULL,
  `MaxPerc` int(11) DEFAULT NULL,
  `MaxIntel` int(11) DEFAULT NULL,
  `MaxLuck` int(11) DEFAULT NULL,
  PRIMARY KEY (`EnemyTypeId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.enemytype: ~14 rows (approximately)
/*!40000 ALTER TABLE `enemytype` DISABLE KEYS */;
INSERT INTO `enemytype` (`EnemyTypeId`, `EnemyTypeName`, `EnemyTypeDescription`, `MaxHP`, `MaxStr`, `MaxPerc`, `MaxIntel`, `MaxLuck`) VALUES
	(1, 'Alien Leader', 'The leader of the aliens is the strongest, oldest and wisest of them all. ', 1500, 10, 10, 10, 10),
	(2, 'Alien Sewer Crawler', 'An alien crawler that\'s a small creature. Seems to like ship vents. Resemble the aliens on some level, so perhaps it\'s a bit like an alien tadpole. Move by jumping using its small tail and two front claws.', 50, 3, 4, 1, 3),
	(3, 'Alien Brawler', 'The alien brawlers are soldiers in training. They must go through a test of courage before they’re allowed to carry ranged weaponry or protection.', 100, 7, 5, 2, 4),
	(4, 'Alien Corporal', 'Aliens recently advanced from brawlers.', 200, 8, 5, 2, 4),
	(5, 'Alien Sergeant', 'Respected members on the alien ship.', 300, 9, 7, 6, 5),
	(6, 'Alien Captain', 'The highest ranking alien officers on board the ship. Captains have undergone extensive training', 400, 10, 8, 8, 5),
	(7, 'Worker Bot', 'A one meter tall pill-shaped blob that moves slowly with its two legs. Disturbingly cute for a shoddily assembled hunk of metal.', 65, 6, 3, 3, 2),
	(8, 'Maintenance Bot', 'Very much like a worker bot except its arms are equipped with a wrench and a laser cutter.', 120, 6, 8, 3, 2),
	(9, 'Crew Service Bot', 'A bot made to serve food and pour drinks for the aliens.', 180, 8, 6, 8, 3),
	(10, 'Standard Guard Bot', 'It’s basically a worker bot with a metal shield on one arm and a laser repeater on the other. Designed to keep peace between crew and to protect the station from intruders.', 250, 6, 8, 5, 5),
	(11, 'Heavy Armament Bot', 'A much bigger robot with extensive metal plating on the body and plasma cannons on each arm. Can really dish out some serious hurt.', 350, 9, 9, 6, 7),
	(12, 'Bullet Sponge Bob', 'It’s basically shaped like a large rectangular block of metal. It has no visible sensors for vision, only one arm with a large plasma cannon attached to it.', 1200, 10, 1, 2, 1),
	(13, 'Evil Leesa', NULL, 800, 8, 8, 8, 8),
	(14, 'Evil Chifundo', NULL, 800, 8, 8, 8, 8);
/*!40000 ALTER TABLE `enemytype` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.item
CREATE TABLE IF NOT EXISTS `item` (
  `ItemId` int(11) NOT NULL,
  `CurrentUseNo` int(11) DEFAULT NULL,
  `PlayerId` int(11) DEFAULT NULL,
  `ItemTypeId` int(11) DEFAULT NULL,
  `EnemyTypeId` int(11) DEFAULT NULL,
  `LocationId` int(11) DEFAULT NULL,
  PRIMARY KEY (`ItemId`),
  KEY `PlayerId` (`PlayerId`),
  KEY `ItemTypeId` (`ItemTypeId`),
  KEY `EnemyTypeId` (`EnemyTypeId`),
  KEY `LocationId` (`LocationId`),
  CONSTRAINT `item_ibfk_1` FOREIGN KEY (`PlayerId`) REFERENCES `playercharacter` (`PlayerId`),
  CONSTRAINT `item_ibfk_2` FOREIGN KEY (`ItemTypeId`) REFERENCES `itemtype` (`ItemTypeId`),
  CONSTRAINT `item_ibfk_3` FOREIGN KEY (`EnemyTypeId`) REFERENCES `enemytype` (`EnemyTypeId`),
  CONSTRAINT `item_ibfk_4` FOREIGN KEY (`LocationId`) REFERENCES `location` (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.item: ~46 rows (approximately)
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` (`ItemId`, `CurrentUseNo`, `PlayerId`, `ItemTypeId`, `EnemyTypeId`, `LocationId`) VALUES
	(1, NULL, NULL, 23, NULL, 102),
	(2, NULL, NULL, 25, NULL, 102),
	(3, NULL, NULL, 2, NULL, 109),
	(4, 1, NULL, 12, NULL, 113),
	(5, 1, NULL, 12, NULL, 113),
	(6, NULL, NULL, 14, NULL, 203),
	(7, 1, NULL, 13, NULL, 203),
	(8, NULL, NULL, 15, NULL, 210),
	(9, NULL, NULL, 16, NULL, 211),
	(10, NULL, NULL, 10, NULL, 211),
	(11, NULL, NULL, 11, NULL, 219),
	(12, NULL, 3, 19, NULL, NULL),
	(13, NULL, 2, 18, NULL, NULL),
	(14, NULL, 1, 17, NULL, NULL),
	(15, NULL, NULL, 1, 2, NULL),
	(16, NULL, NULL, 3, 3, NULL),
	(17, NULL, NULL, 9, 4, NULL),
	(18, NULL, NULL, 14, 4, NULL),
	(19, NULL, NULL, 10, 5, NULL),
	(20, NULL, NULL, 15, 5, NULL),
	(21, NULL, NULL, 11, 6, NULL),
	(22, NULL, NULL, 16, 6, NULL),
	(23, NULL, NULL, 11, 1, NULL),
	(24, NULL, NULL, 16, 1, NULL),
	(25, NULL, NULL, 2, 7, NULL),
	(26, NULL, NULL, 7, 8, NULL),
	(27, NULL, NULL, 3, 9, NULL),
	(28, NULL, NULL, 8, 10, NULL),
	(29, NULL, NULL, 9, 11, NULL),
	(30, NULL, NULL, 9, 12, NULL),
	(31, NULL, NULL, 16, 12, NULL),
	(32, NULL, NULL, 15, 11, NULL),
	(33, NULL, NULL, 15, 10, NULL),
	(34, NULL, NULL, 15, 9, NULL),
	(35, NULL, NULL, 14, 8, NULL),
	(36, NULL, NULL, 14, 7, NULL),
	(37, NULL, 1, 1, NULL, NULL),
	(38, NULL, 2, 1, NULL, NULL),
	(39, NULL, 3, 1, NULL, NULL),
	(40, NULL, NULL, 24, NULL, 214),
	(41, NULL, NULL, 26, NULL, 220),
	(42, NULL, NULL, 7, NULL, NULL),
	(43, NULL, NULL, 5, NULL, NULL),
	(44, NULL, NULL, 4, NULL, NULL),
	(45, NULL, NULL, 10, 14, NULL),
	(46, NULL, NULL, 10, 13, NULL);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.itemtype
CREATE TABLE IF NOT EXISTS `itemtype` (
  `ItemTypeId` int(11) NOT NULL,
  `ItemTypeName` varchar(50) DEFAULT NULL,
  `ItemTypeDescription` varchar(2000) DEFAULT NULL,
  `DmgReduction` float DEFAULT NULL,
  `MinDmg` float DEFAULT NULL,
  `MaxDmg` float DEFAULT NULL,
  `DmgToStr` int(11) DEFAULT NULL,
  `DmgToPerc` int(11) DEFAULT NULL,
  `DmgToIntel` int(11) DEFAULT NULL,
  `DmgToLuck` int(11) DEFAULT NULL,
  `AddStr` int(11) DEFAULT NULL,
  `AddPerc` int(11) DEFAULT NULL,
  `AddIntel` int(11) DEFAULT NULL,
  `AddLuck` int(11) DEFAULT NULL,
  `IsArmor` int(11) DEFAULT NULL,
  `IsWeapon` int(11) DEFAULT NULL,
  `IsUsable` int(11) DEFAULT NULL,
  `AbilityId` int(11) DEFAULT NULL,
  PRIMARY KEY (`ItemTypeId`),
  KEY `AbilityId` (`AbilityId`),
  CONSTRAINT `itemtype_ibfk_1` FOREIGN KEY (`AbilityId`) REFERENCES `ability` (`AbilityId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.itemtype: ~26 rows (approximately)
/*!40000 ALTER TABLE `itemtype` DISABLE KEYS */;
INSERT INTO `itemtype` (`ItemTypeId`, `ItemTypeName`, `ItemTypeDescription`, `DmgReduction`, `MinDmg`, `MaxDmg`, `DmgToStr`, `DmgToPerc`, `DmgToIntel`, `DmgToLuck`, `AddStr`, `AddPerc`, `AddIntel`, `AddLuck`, `IsArmor`, `IsWeapon`, `IsUsable`, `AbilityId`) VALUES
	(1, 'Unarmed', 'It is your bare fists.', NULL, 10, 15, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(2, 'Carbon Fiber Knife', 'A lightweight knife made of carbon fiber. Good for spreading butter, though could perhaps be used as a weapon in a pinch.', NULL, 13, 17, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(3, 'Alien Alloy Spear', 'A spear made of a mysterious metal-like material.', NULL, 17, 19, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(4, 'Ballistic Pistol', 'An old ballistic pistol. Apparently objects travelling very fast still hurt.', NULL, 17, 23, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(5, 'Ballistic Submachinegun', 'Ballistic submachinegun. Spray and pray!', NULL, 15, 32, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(6, 'Ballistic Semi-Automatic Rifle', 'This rifle has seen better days. Effective, long as it doesn\'t get jammed.', NULL, 23, 38, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(7, 'Laser Pistol', 'A fairly new laser pistol. Coating has seen better days, but all the functional parts look almost new.', NULL, 19, 27, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(8, 'Laser Semi-Automatic Rifle', 'A semi-automatic laser rifle. Fires bursts of three laser beams at a time.', NULL, 26, 46, NULL, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(9, 'Alien Plasma Pistol', 'Never seen anything like it. Plasma fills a transparent chamber at the back of the gun before it\'s launched at high velocity from the barrel.', NULL, 23, 32, 1, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(10, 'Alien Semi-Automatic Plasma Rifle', 'Has 3 large chambers with plasma that are emptied almost instantly.', NULL, 30, 60, 1, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(11, 'Alien Plasma Gatling Gun', 'Has 12 medium-sized plasma chambers around the circumference of the gun\'s body. Short heat-up time after the last chamber is emptied.', NULL, 23, 90, 1, 1, 1, 1, NULL, NULL, NULL, NULL, NULL, 1, NULL, NULL),
	(12, 'HE-Grenade', 'Standard military-grade high-explosive grenade. Everyone in the vicinity suffers damage from the blast.', NULL, 15, 50, 1, 1, 1, 3, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL),
	(13, 'High-Explosive Charge ', 'Large block of high-explosive material. Hopefully it won\'t explode in your backpack. Damages eveyone in the vicinity of the blast.', NULL, 35, 70, 2, 1, 2, 1, NULL, NULL, NULL, NULL, NULL, NULL, 1, NULL),
	(14, 'Light Alien Armor', 'Light Alien armor made up of 3 smaller parts. Material feels like metal but looks like plastic.', 0.9, NULL, NULL, NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(15, 'Medium Alien Armor', 'Medium Alien armor made up of 3 medium-sized parts. Material is plastic-looking metal with a thin layer of weaved fabrics beneath the plating.', 0.85, NULL, NULL, NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(16, 'Heavy Alien Armor', 'Full body Alien armor made of a very heavy ceramic-like material. On top of the ceramic there\'s a hexa-pattern made of plastic-looking metal. Beneath the ceramic there\'s a medium layer of tightly weaved fabric. Bet it\'s hot in there.', 0.75, NULL, NULL, NULL, NULL, NULL, NULL, 7, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(17, 'Trash Hauler Space Suit ', 'Standard Trash Hauler Space Suit. This one\'s garbage-stained from top to bottom.', 0.95, NULL, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(18, 'Light Mercenary Armor', 'Standard PMC-equipment from 30 years ago. Not unknown to combat, this one\'s riddled with bullet holes and laser burns.', 0.88, NULL, NULL, NULL, NULL, NULL, NULL, 3, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(19, 'Light Civilian Armor ', 'A light armor that can be purchased by anyone anywhere. Only 31 million pieces of this model has been sold in the system making it the most non-descript piece of armor available. Popular among the shady types who prefer to go unnoticed.', 0.92, NULL, NULL, NULL, NULL, NULL, NULL, 2, NULL, NULL, NULL, 1, NULL, NULL, NULL),
	(20, 'Quantum-Luck Prototype ', 'Prototype of an augment that uses quantum effects to somehow result in more positive outcomes for the wearer. No one understands exactly how it works and no other prototypes are known to exist.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 1, 1, NULL, NULL, NULL, NULL),
	(21, 'HeavyLifter Mech-Arm v.3325.1 ', 'An over 20-year old model of HeavyLifter\'s popular Mech-Arm lineup. This one has seen some wear and tear to put it lightly.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3, 2, NULL, NULL, NULL, NULL, NULL, NULL),
	(22, 'Xchip Vulnerability Scanner', 'An old vulnerability scanner that\'s been outlawed since then. Capable of hacking most electronic systems given physical access.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 3, 2, NULL, NULL, NULL, NULL, NULL),
	(23, 'Keycard (Jail Cell)', 'A number 1 informs me that the keycard has only a single use remaining.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(24, 'Keycard (Upper Elevator)', 'Opens the elevator on Admin corridor.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(25, 'CD', 'An old cd that has Windows Vista written on it.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
	(26, 'Keycard (Engine control room)', 'Opens the engine control room on floor -1.', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
/*!40000 ALTER TABLE `itemtype` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.location
CREATE TABLE IF NOT EXISTS `location` (
  `LocationId` int(11) NOT NULL,
  `LocationName` varchar(50) NOT NULL,
  `LocDescription` varchar(2000) DEFAULT NULL,
  `SurpriseTrigger` int(11) DEFAULT NULL,
  PRIMARY KEY (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.location: ~37 rows (approximately)
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` (`LocationId`, `LocationName`, `LocDescription`, `SurpriseTrigger`) VALUES
	(101, 'Jaw', 'The jaw of this ship!', 0),
	(102, 'Jaw storage', 'Upon walking in you realize your own trash ship is there. It looks pretty TRASHED so there’s no way you could fly it back home.\r\n	 Not to mention at the back is a huge jaw-like hatch that\r\n	  was probably used to capture you and your ship. \r\n	  There’s also lots of other small debris and metal junk laying around. This must be some \r\n	  kind of debris collecting ship. \r\n	  But why have the ones operating this ship captured you along with \r\n	  other people?', 0),
	(103, 'Corridor (Floor -1)', 'This room must be some kind of corridor. There are plenty \r\n	of paths to explore. The \r\n	 room has similar style as other corridors with blueish \r\n	 bright lights and mirror-like floor. The humming is \r\n	 getting louder and it seems to be coming from above.', 0),
	(104, 'Elevator', 'You are in an elevator.', 0),
	(105, 'Your cell', 'You hear rather loud engine humming \r\n	from above. The “cell”, if you call it that, looks like\r\n	 a janitor’s room. It’s dimly lit with mops,  brooms\r\n	  and a machine that might be a vacuum laying around. \r\n	  The door has a small window on it and next to it is a button,\r\n	   that displays a green light.', 0),
	(106, 'Man Cell', 'The cell has a small surface coming from the wall, which is probably intended for sleeping, and a toilet. Hopefully the giant isn’t claustrophobic.', 0),
	(107, 'Woman cell', 'The cell has a small surface coming from the wall, which is probably intended for sleeping, and a toilet.', 0),
	(108, 'Corridor  (Floor 0)', 'You can barely hear your words over this ear-bleeding noise! The sound\r\n	is coming from your left. The style continues the same with mirror-like floor and blue lights on walls. ', 0),
	(109, 'Engine bay', 'The humming is at it\'s absolute maximum now and you feel like you will go deaf any second now. \r\n	You see engines running. You remember seeing something like that in history books. It\r\n	 looks like a V8. Ancient human automobiles used those kind of machines, except this one is much bigger. They had great growling sound unlike space cars of today.', 0),
	(110, 'Cockpit corridor', '', 0),
	(111, 'Cockpit', '', 0),
	(112, 'Corridor  (Floor 1)', 'You see straight-as-an-arrow corridor. There are small windows on the wall. You don\'t recognize any of the planets. Where the hell is this ship going?', 1),
	(113, 'Cabin', 'You see bunks and locket cabinets. This must be cabin for the crew!', 0),
	(114, 'Cabin2', '', 0),
	(115, 'Escape pod room', 'As you enter your eye is immediately lead to weird machines next to the wall. They might be escape pods! Maybe you should use the pods to escape the ship?', 0),
	(201, 'Ship park', 'Your ship is parked in this huge space. Surely this must be a ship park.', 0),
	(202, 'Hangar corridor (Floor 0)', 'A round corridor. Unlike last ship this is very dark and the walls almost look like they\'re made of rock but can that really be the rock you know? You walk around the corridor and see two doors. The other one must be an elevator. There\'s also loads of doors leading to other ship parks but they\'re all locked.', 0),
	(203, 'Janitor\'s closet', 'Cramped space with brooms and mops.', 2),
	(204, 'Main elevator', 'You are in an elevator.', 0),
	(205, 'Engine control room corridor  (Floor -1)', 'Similar to the other corridor this, too, has the weird\r\n	 rock walls. There\'s also a faint humming.', 0),
	(206, 'Engine control room', 'You see a massive computer station with loads of flickering lights in different colors. There is a CD drive on the computer.', 0),
	(207, 'Power supply corridor (Floor -2)', 'Another corridor! This is exactly the same as the others...', 0),
	(208, 'Power supply room', 'You see massive station of screens displaying graphs of data. There is a console on one of the computers. It looks like you could use it for something.', 0),
	(209, 'Crew barracks corridor (Floor 1)', 'This corridor has still rock-like walls but surprisingly there\'s \r\n	some plants. The ecosystem is truly thriving!', 0),
	(210, 'Secret room', 'Absolutely tiny space and dark place. What is even the purpose of this room??', 1),
	(211, 'Armory', 'You hit the jackpot! There\'s so many weapons and armour here you can\'t believe it!\r\n	 With these the aliens could easily destroy humans for good. ...It\'s a shame most of them are locked behind cabinets.', 0),
	(212, 'Crew cafeteria', 'It faintly reminds you of your elementary school\'s cafeteria. Not a pretty sight.', 0),
	(213, 'Admin corridor (Floor 2)', 'Long corridor that makes a sharp turn.', 2),
	(214, 'Security room', 'What can I say? It\'s like a NASA control room. Computers and stuff.\r\n	 Which is weird since you haven\'t seen any surveillance cameras.', 2),
	(215, 'Telecommunications room', 'More computers! You see a telecomm in the room. You could probably use the telecom to send a message to the human HQ!', 0),
	(216, '???', '', 0),
	(217, 'Upper elevator', 'You are in an elevator.', 0),
	(218, 'Cockpit (Floor 3)', '', 0),
	(219, 'Commander suite (Floor 4)', 'You enter in a room. It is oddly furnitured. There are benches and beds in \r\n	Victorian style but also functionalist shelves and a traffic rug that\'s usually found in kid\'s rooms.\r\n	 In the middle is a door that leads hopefully to the guy who is behind all this.', 0),
	(220, 'Command tower', 'This must be the place where everything is controlled in the space station. You don\'t see a CD drive on any of the computers in the room. ', 0),
	(301, 'Accept', NULL, 0),
	(302, 'Cancel', NULL, 0);
/*!40000 ALTER TABLE `location` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.passage
CREATE TABLE IF NOT EXISTS `passage` (
  `PassageId` varchar(100) NOT NULL,
  `Locked` int(11) DEFAULT NULL,
  `LockPrompt` varchar(500) DEFAULT NULL,
  `HackableLock` int(11) DEFAULT NULL,
  `LockCode` bigint(20) DEFAULT NULL,
  `DepartureLoc` int(11) NOT NULL,
  `ArrivalLoc` int(11) NOT NULL,
  PRIMARY KEY (`PassageId`),
  KEY `DepartureLoc` (`DepartureLoc`),
  KEY `ArrivalLoc` (`ArrivalLoc`),
  CONSTRAINT `passage_ibfk_1` FOREIGN KEY (`DepartureLoc`) REFERENCES `location` (`LocationId`),
  CONSTRAINT `passage_ibfk_2` FOREIGN KEY (`ArrivalLoc`) REFERENCES `location` (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.passage: ~56 rows (approximately)
/*!40000 ALTER TABLE `passage` DISABLE KEYS */;
INSERT INTO `passage` (`PassageId`, `Locked`, `LockPrompt`, `HackableLock`, `LockCode`, `DepartureLoc`, `ArrivalLoc`) VALUES
	('10_9', 0, 'This door is open.', 0, 0, 210, 209),
	('11_9', 0, 'This door is open.', 0, 0, 211, 209),
	('12-13', 1, 'This door is locked. It looks like it could be hacked though.', 1, 12683, 112, 113),
	('12-14', 1, 'This door is locked.', 0, 0, 112, 112),
	('12-15', 0, 'This door is open.', 0, 0, 112, 115),
	('12-4', 0, 'This door is open.', 0, 0, 112, 104),
	('12_9', 0, 'This door is open.', 0, 0, 212, 209),
	('13-12', 0, 'This door is open.', 0, 0, 113, 112),
	('13_14', 1, 'This door is locked. It looks hackable though.', 1, 6300, 213, 214),
	('13_15', 0, 'This door is open.', 0, 0, 213, 215),
	('13_17', 1, 'This door is locked. It has a slot for keycard.', 0, 0, 213, 217),
	('13_4', 0, 'This door is open.', 0, 0, 213, 204),
	('14_13', 0, 'This door is open.', 0, 0, 214, 213),
	('15-12', 1, 'This door is open.', 0, 0, 115, 112),
	('15_13', 0, 'This door is open.', 0, 0, 215, 213),
	('17_13', 0, '', 0, 0, 217, 213),
	('17_19', 0, '', 0, 0, 217, 219),
	('19_17', 0, 'This door is open.', 0, 0, 219, 217),
	('19_20', 0, 'This door is open.', 0, 0, 219, 220),
	('1_2', 0, 'This door is open.', 0, 0, 201, 202),
	('2-3', 0, 'This door is open.', 1, 4875, 102, 103),
	('20_19', 0, 'This door is open.', 0, 0, 220, 219),
	('2_1', 0, 'This door is open.', 0, 0, 202, 201),
	('2_3', 1, 'This door is locked. It looks like it could be hacked though.', 1, 68396, 202, 203),
	('2_4', 0, 'This door is open.', 0, 0, 202, 204),
	('3-2', 1, 'This door is locked. It looks like it could be hacked though.', 1, 487, 103, 102),
	('3-4', 1, 'This door is locked. This one doesn\'t look hackable.', 0, 0, 103, 104),
	('3-5', 0, 'The cell door is open for some reason.', 0, 0, 103, 105),
	('3-6', 1, 'This door is locked. It has a slot for a keycard though.', 0, 0, 103, 106),
	('3-7', 1, 'This door is locked. It has a slot for a keycard though.', 0, 0, 103, 107),
	('3_2', 0, 'This door is open.', 0, 0, 203, 202),
	('4-12', 0, '', 0, 0, 104, 112),
	('4-3', 0, '', 0, 0, 104, 103),
	('4-8', 0, '', 0, 0, 104, 108),
	('4_13', 0, '', 0, 0, 204, 213),
	('4_2', 0, '', 0, 0, 204, 202),
	('4_5', 0, '', 0, 0, 204, 205),
	('4_7', 0, '', 0, 0, 204, 207),
	('4_9', 0, '', 0, 0, 204, 209),
	('5-3', 0, '', 0, 0, 105, 103),
	('5_4', 0, 'This door is open.', 0, 0, 205, 204),
	('5_6', 1, 'This door is locked. It has a slot for keycard.', 0, 0, 205, 206),
	('6-3', 0, 'This door is open.', 0, 0, 106, 103),
	('6_5', 0, 'This door is open.', 0, 0, 206, 205),
	('7-3', 0, 'This door is open.', 0, 0, 107, 103),
	('7_4', 0, 'This door is open.', 0, 0, 207, 204),
	('7_8', 0, 'This door is open.', 0, 0, 207, 208),
	('8-10', 1, 'This door is locked.', 0, 0, 108, 108),
	('8-4', 0, 'This door is open.', 0, 0, 108, 104),
	('8-9', 1, 'This door is locked. It looks like it could be hacked though.', 1, 98986, 108, 109),
	('8_7', 0, 'This door is open.', 0, 0, 208, 207),
	('9-8', 0, 'This door is open.', 0, 0, 109, 108),
	('9_10', 1, 'This door is locked. It looks hackable though.', 1, 42983, 209, 210),
	('9_11', 1, 'This door is locked. It looks... kinda hackable...', 1, 1599991881, 209, 211),
	('9_12', 0, 'This door is open. You can hear lots of speech behind it. It\'s probably best not to open this door.', 0, 0, 209, 212),
	('9_4', 0, 'This door is open.', 0, 0, 209, 204);
/*!40000 ALTER TABLE `passage` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.playercharacter
CREATE TABLE IF NOT EXISTS `playercharacter` (
  `PlayerId` int(11) NOT NULL,
  `PlayerName` varchar(50) DEFAULT NULL,
  `MaxHP` float DEFAULT NULL,
  `CurrentHP` float DEFAULT NULL,
  `MaxStr` int(11) DEFAULT NULL,
  `CurrentStr` int(11) DEFAULT NULL,
  `MaxPerc` int(11) DEFAULT NULL,
  `CurrentPerc` int(11) DEFAULT NULL,
  `MaxIntel` int(11) DEFAULT NULL,
  `CurrentIntel` int(11) DEFAULT NULL,
  `MaxLuck` int(11) DEFAULT NULL,
  `CurrentLuck` int(11) DEFAULT NULL,
  `Armor` int(11) DEFAULT NULL,
  `Weapon` int(11) DEFAULT NULL,
  `LocationId` int(11) DEFAULT NULL,
  PRIMARY KEY (`PlayerId`),
  KEY `LocationId` (`LocationId`),
  KEY `playercharacter_ibfk_2` (`Armor`),
  KEY `playercharacter_ibfk_3` (`Weapon`),
  CONSTRAINT `playercharacter_ibfk_1` FOREIGN KEY (`LocationId`) REFERENCES `location` (`LocationId`),
  CONSTRAINT `playercharacter_ibfk_2` FOREIGN KEY (`Armor`) REFERENCES `item` (`ItemId`),
  CONSTRAINT `playercharacter_ibfk_3` FOREIGN KEY (`Weapon`) REFERENCES `item` (`ItemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.playercharacter: ~3 rows (approximately)
/*!40000 ALTER TABLE `playercharacter` DISABLE KEYS */;
INSERT INTO `playercharacter` (`PlayerId`, `PlayerName`, `MaxHP`, `CurrentHP`, `MaxStr`, `CurrentStr`, `MaxPerc`, `CurrentPerc`, `MaxIntel`, `CurrentIntel`, `MaxLuck`, `CurrentLuck`, `Armor`, `Weapon`, `LocationId`) VALUES
	(1, 'Pan Bannister', 200, 200, 5, 5, 4, 4, 4, 4, 10, 10, 14, 37, 105),
	(2, 'Chifundo', 250, 250, 10, 10, 7, 7, 1, 1, 4, 4, 13, 38, 106),
	(3, 'Leesa', 150, 150, 2, 2, 8, 8, 10, 10, 3, 3, 12, 39, 107);
/*!40000 ALTER TABLE `playercharacter` ENABLE KEYS */;

-- Dumping structure for table odyssey3348.storycontainer
CREATE TABLE IF NOT EXISTS `storycontainer` (
  `StoryId` int(11) NOT NULL,
  `Textblock` varchar(10000) DEFAULT NULL,
  `VariationId` int(11) DEFAULT NULL,
  `LocationId` int(11) DEFAULT NULL,
  `Used` int(11) DEFAULT NULL,
  KEY `VariationId` (`VariationId`),
  KEY `LocationId` (`LocationId`),
  CONSTRAINT `storycontainer_ibfk_1` FOREIGN KEY (`VariationId`) REFERENCES `playercharacter` (`PlayerId`),
  CONSTRAINT `storycontainer_ibfk_2` FOREIGN KEY (`LocationId`) REFERENCES `location` (`LocationId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table odyssey3348.storycontainer: ~34 rows (approximately)
/*!40000 ALTER TABLE `storycontainer` DISABLE KEYS */;
INSERT INTO `storycontainer` (`StoryId`, `Textblock`, `VariationId`, `LocationId`, `Used`) VALUES
	(0, 'Commands:\nmove (room)\npick up (item)\nhack (room)\ninventory\nequip (item)\nuse (object)\nlook room\nexamine (item)\n\nFor an example if you are in an elevator you can just\ninput the floor (move floor 1)\n\nThe use command can be used with some objects in your \ninventory and with some objects in the room.\n\nCombat:\n\nattack (enemy name)\nuse (list usables and amount)\nuse grenade\nuse charge\n\nIn combat you can just type "attack" to attack the first enemy.\nIf you want to repeat your last command in combat\nyou can type "p" to do this.\n\n', 1, NULL, 0),
	(1, '“Good morning galaxy! You are listening to Galaxy News Radio 5 and I hope you are feeling nice where ever you may be in space and time. Today’s earth-date is 7th of June 3348 and we’ll start the broadcast with the best of the 21st-century playlist.”, rattles from the radio in the starship’s cockpit.', 1, 105, 0),
	(2, '“What trash..”, escape your mouth as you start switching the channel on the radio but finding nothing worth listening. There is irony in your words as you yourself literally work with trash. You are an intergalactic trash hauler by the name of Pan Bannister. Equipped with the most average body build, the company’s overalls and a safety hat you slouch on the “captain’s chair” wondering how to pass the time until the next stop.', 1, 105, 0),
	(3, 'You receive a hail on your ship’s com. You hear language unknown to you and you see dark shadow appear on around your cockpit window. The shadow seems to be the huge jaws of the alien ship closing around you with your ship trapping inside. The jaws close and the ship begins to rumble as it is magnetically pulled into an open spot on the floor inside a huge bay of the alien ship.', 1, 105, 0),
	(4, 'You see all kinds of human ships in the bay. These must be other ships the aliens have “eaten” before you. Your gaze comes across a group of rats that approach your ship. These weren’t ordinary rats for they were fully clothed, running on 2 feet and holding what you guess to be some sort of weapons. You hear sounds coming outside from your cockpit door. “What in the…”, you say as the door explodes open and the blast knocks you unconscious.', 1, 105, 0),
	(5, 'You open your eyes and you see that you are in a cell. “You pesky furry bastards! Let me out of here at once!”, you hear a woman say. “Yeah! That’s right!”, a more manly voice joined. “Hello? What’s going on here?”, you ask. “What do you think? These damn rats ate our ship and now we are traped in these cells..", said the woman. "Try and see if you can get out!" said the mans voice "We have already tried to get out of our cells". ', 1, 105, 0),
	(7, 'You insert the keycard into a slot next to the cell door and the cell door opens. "Thank god! Finally a face without a snout! I\'m Leesa by the way". You take the keycard from the slot. The card now shows a zero on the display. Leesa looks at you and says "Well I guess it\'s you and me now. Let me take a look in here... I think I can open this elevator for us." She opens a panel next to the elevator and her hands pick apart the insides of the panel. Like magic the elevator door is now open. "Told ya!", she said with a smerk on her face.', 3, 103, 0),
	(7, 'You insert the keycard into a slot next to the cell door and the cell door opens. "Oh! I\'m free! Thank you sir! I\'m called Chifundo!". You take the keycard from the slot. The card now shows a zero on the display. Chifundo looks at you and says "Looks like it\'ll be a sausage fest heh..". Chifundo walks to the center of the corridor and looks around while scratching his head. He then goes to the elevator door and pulls the door open with his mechanical arm. "I was hoping for some action but atleast we can use the elevator now heh..".', 2, 103, 0),
	(6, 'Like a miracle the door to your cell is left open. Must be the doing of your Quantum-Luck –augment in your head.', 1, 103, 0),
	(10, 'You and Chifundo go inside your own pods. The pod door shuts and it launches into space. As you look out of the pod door window you hear a weird hum inside the pod. Suddenly you feel extremely cold. Before you fully realize what is happening the temperature drops to subzero and you are frozen solid. The pod was a cryo-pod and you now float aimlessly in space.', 2, 201, 0),
	(10, 'You and Leesa go inside your own pods. The pod door shuts and it launches into space. As you look out of the pod door window you hear a weird hum inside the pod. Suddenly you feel extremely cold. Before you fully realize what is happening the temperature drops to subzero and you are frozen solid. The pod was a cryo-pod and you now float aimlessly in space.', 3, 201, 0),
	(11, '200 years have passed since you got into your pod. Your frozen journey has met its end as your pod is spotted by a passing ship. The pod is sucked into the ship and it continues its course.', 1, 201, 0),
	(12, 'You regain consciousness and a feeling of relief takes over you as you see a circle of humans surrounding the bed you are on. “Pan? Pan Bannister? Is it really you?”, you hear one of them say. “Chifundo?”, you say in disbelieve. Your eyes are not lying as you see Chifundo in what seems to be an army uniform.', 2, 201, 0),
	(12, 'You regain consciousness and a feeling of relief takes over you as you see a circle of humans surrounding the bed you are on. “Pan? Pan Bannister? Is it really you?”, you hear one of them say. “Leesa?”, you say in disbelieve. Your eyes are not lying as you see Leesa in what seems to be an army uniform.', 3, 201, 0),
	(13, '“I was drifting in space and was found by the Humanity’s Rebellion about 20 years ago. One thing led to another and I’m now the general of humanity’s last hope”, Leesa tells you that around the time you both were abducted by the aliens they started an invasion on the galaxy. Almost the whole human race is under alien control and the rebellion is the last force fighting the aliens. You can see why Leesa is in this position.', 3, 201, 0),
	(13, '“I was drifting in space and was found by the Humanity’s Rebellion about 20 years ago. One thing led to another and I’m now the general of humanity’s last hope”, Chifundo tells you that around the time you both were abducted by the aliens they started an invasion on the galaxy. Almost the whole human race is under alien control and the rebellion is the last force fighting the aliens. You can’t wrap your head around the fact that Chifundo is now an army general. Times really seem desperate.\r\n', 2, 201, 0),
	(14, 'Leesa shows you to your cabin and you start unpacking your things on a desk. As you unpack Leesa notices the CD you placed on the desk from your pockets. “That CD, it could be useful. Everything from the old days are destroyed by the aliens. The R&D department would appreciate if they could take a look?” says Leesa. You give the CD to Leesa and she leaves you.', 3, 201, 0),
	(14, 'Chifundo shows you to your cabin and you start unpacking your things on a desk. As you unpack Chifundo notices the CD you placed on the desk from your pockets. “That CD, it could be useful. Everything from the old days are destroyed by the aliens. The R&D department would appreciate if they could take a look heh?” says Chifundo. You give the CD to Chifundo and he leaves you.', 2, 201, 0),
	(15, 'Your eyes feel heavy even thou you basically slept for 200 years. There is a bed in your cabin and you jump into the sheets. The moment your body touches the soft surface of the bed you fall asleep.', 1, 201, 0),
	(16, 'Next day Leesa wakes you up with excitement. The R&D department found that the CD you had is an ancient operating system for old binary computers. It is called “Windows Vista” and the coding was so twisted and bad that it melted the quantum computer that tried to execute it. Leesa believes that if the CD could be uploaded into the mainframe in the alien HQ, it could render the aliens defenseless against an attack. It could be the salvation of the humanity! You eagerly volunteer for the mission and the next day you and Leesa embark with a small fleet of fighter ships into alien territory. You all jump into warp speed.', 3, 201, 0),
	(16, 'Next day Chifundo wakes you up with excitement. The R&D department found that the CD you had is an ancient operating system for old binary computers. It is called “Windows Vista” and the coding was so twisted and bad that it melted the quantum computer that tried to execute it. Chifundo believes that if the CD could be uploaded into the mainframe in the alien HQ, it could render the aliens defenseless against an attack.  It could be the salvation of the humanity! You eagerly volunteer for the mission and the next day you and Chifundo embark with a small fleet of fighter ships into alien territory. You all jump into warp speed.', 2, 201, 0),
	(17, 'The fleet drops from warp speed close to the alien HQ space station. The fleet of fighters protect the ship you and Leesa are on as you come closer to the station but even with everyone’s best efforts your ship is hit badly and you lose all control. Your ship crashes uncontrollably into the station. Luckily your ship crashes into the space station’s parking area.', 3, 201, 0),
	(17, 'The fleet drops from warp speed close to the alien HQ space station. The fleet of fighters protect the ship you and Chifundo are on as you come closer to the station but even with everyone’s best efforts your ship is hit badly and you lose all control. Your ship crashes uncontrollably into the station. Luckily your ship crashes into the space station’s parking area.', 2, 201, 0),
	(30, 'You insert the CD into the drive of the mainframe. A prompt appears in one off the screens which has two options; Accept and Cancel. Before you can do anything the door to the room opens and you see an old rat with a white beard. “Stop whatever it is you are doing!”, the old rat says, “I’m the leader of my people and I will not let you destroy what we have built for hundreds of years. If you stop and surrender, we will give you anything your heart desires.” “Anything?”, you ask. “Anything.”, the leader sighs.', 1, 206, 1),
	(31, 'You press Accept on the screen and the whole space station starts to rumble. An explosion blasts the rat leader into small dust and you and Leesa start to run your way into the hangar. When you two make it to the hangar it is full of the rat aliens. “Go Leesa! I’ll deal with this.”, you say as you run into the swarm of rats. Leesa nods and runs to your ship and waits for you there for a moment but the hangar is filled with fire, smoke and explosions. Leesa decides to leave without you and as she looks at the destroying space station she says aloud, “I know you’ll survive. No one is as lucky as you Pan.”', 3, 301, 0),
	(31, 'You press Accept on the screen and the whole space station starts to rumble. An explosion blasts the rat leader into small dust and you and Chifundo start to run your way into the hangar. When you two make it to the hangar it is full of the rat aliens. “Go Chifundo! I’ll deal with this.”, you say as you run into the swarm of rats. Chifundo nods and runs to your ship and waits for you there for a moment but the hangar is filled with fire, smoke and explosions. Chifundo decides to leave without you and as he looks at the destroying space station he says aloud, “I know you’ll survive. No one is as lucky as you Pan.”', 2, 301, 0),
	(31, 'You press Cancel on the screen. The leader approaches you with a big smile on his face. “Well done.”, the alien leader says while pulling a gun to your chest. “Never trust a rat I guess..”, the rat leader laughs and pulls the trigger', 1, 302, 0),
	(20, '“Look who it is…”, you hear a somewhat familiar voice say. “You might not know me Pan, but I sure do know you.” A shadowy figure appears from the back of the room. “You don’t know the hell I have had to go through because of you..”, the shadow continues. “Who are you?”, you say. “I’m the one you left to rot in that cell 200 years ago , remember?”, the shadow says.', 1, 220, 0),
	(21, '“I’m Leesa by the way. You might be thinking why I’m alive all these years? Well these lovely rats did some experiments on me and now I’m an immortal slave to these rats, but I guess I can forgive them now. I’ll get my revenge now!”', 2, 220, 0),
	(21, '“I’m called Chifundo. You might be thinking why I’m alive all these years? Well these lovely rats did some experiments on me and now I’m an immortal slave to these rats, but I guess I can forgive them now. I’ll get my revenge now!”', 3, 220, 0),
	(18, 'You fiddle with the console and somehow you manage to reroute the power to unlock the armory door! Lucky!', 1, 208, 1),
	(19, 'You insert the keycard into the slot next to the elevator and the elevator door opens!', 1, 213, 1),
	(22, 'You manage to get the telecom to work and you now have a direct line to the human rebellion. "Pan? Is that you? What the hell are you doing? Go find a CD drive on that station!", someone yells to you on the other end. "Yeah I know.. I just wanted to say hi.", you say and disconnect the telecomm. ', 1, 215, 1),
	(23, 'You insert the keycard into the slot next to the door and the door opens!', 1, 205, 1);
/*!40000 ALTER TABLE `storycontainer` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;