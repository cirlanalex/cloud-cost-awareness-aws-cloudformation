-- --------------------------------------------------------
-- Host:                         localhost
-- Server version:               11.4.2-MariaDB-ubu2404 - mariadb.org binary distribution
-- Server OS:                    debian-linux-gnu
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Dumping structure for table cloudformation.commits
CREATE TABLE IF NOT EXISTS `commits` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `repo_id` bigint(50) NOT NULL,
  `url` varchar(300) NOT NULL,
  `hash` varchar(100) NOT NULL,
  `has_non_template` enum('Yes','No') NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_url` (`url`),
  KEY `FK_commits_repos` (`repo_id`),
  CONSTRAINT `FK_commits_repos` FOREIGN KEY (`repo_id`) REFERENCES `repos` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table cloudformation.commits: ~0 rows (approximately)

-- Dumping structure for table cloudformation.keywords
CREATE TABLE IF NOT EXISTS `keywords` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table cloudformation.keywords: ~6 rows (approximately)
INSERT INTO `keywords` (`id`, `name`) VALUES
	(1, 'bill'),
	(2, 'cheap'),
	(3, 'cost'),
	(4, 'efficient'),
	(5, 'expens'),
	(6, 'pay');

-- Dumping structure for table cloudformation.keywords_commits
CREATE TABLE IF NOT EXISTS `keywords_commits` (
  `keyword_id` bigint(20) NOT NULL,
  `commit_id` bigint(20) NOT NULL,
  UNIQUE KEY `UK_keywords_commits` (`keyword_id`,`commit_id`),
  KEY `FK_commits_keywords` (`commit_id`),
  KEY `FK_keywords_commits` (`keyword_id`),
  CONSTRAINT `FK_commits_keywords` FOREIGN KEY (`commit_id`) REFERENCES `commits` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK_keywords_commits` FOREIGN KEY (`keyword_id`) REFERENCES `keywords` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table cloudformation.keywords_commits: ~0 rows (approximately)

-- Dumping structure for table cloudformation.repos
CREATE TABLE IF NOT EXISTS `repos` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `url` varchar(200) NOT NULL,
  `flag` enum('none','aws','error','skipped','missing') NOT NULL DEFAULT 'none',
  `stop_stage` enum('yaml','aws') DEFAULT NULL,
  `truncated_1k` enum('Yes','No') DEFAULT NULL,
  `truncated_10k` enum('Yes','No') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UK_url` (`url`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Dumping data for table cloudformation.repos: ~0 rows (approximately)

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
