-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: botdb
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `questiontab`
--

DROP TABLE IF EXISTS `questiontab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questiontab` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `question` varchar(255) DEFAULT NULL,
  `idContext` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questiontab`
--

LOCK TABLES `questiontab` WRITE;
/*!40000 ALTER TABLE `questiontab` DISABLE KEYS */;
INSERT INTO `questiontab` VALUES (18,'Привет',10),(19,'Здравствуй',10),(20,'Как дела',11),(21,'Че как',11),(22,'Что делаешь',12),(23,'Сколько время',13),(25,'Тест',14),(26,'Проверка',15),(27,'Как жизнь?',11),(28,'Приветствую',10),(29,'Запусти режим беседы',16),(30,'Давай побеседуем',16),(32,'Давай поболтаем',16),(33,'Активируй модуль ИИ',16),(34,'Кто ты?',17),(35,'Что ты?',17),(36,'Перейди в режим ии',16),(37,'Кто я?',18),(38,'Что ты обо мне знаешь?',18),(39,'Какие сегодня пары?',19),(40,'Расписание на сегодня?',19),(41,'Какая сейчас неделя?',20),(42,'Какая идет неделя?',20),(45,'Расписание на текущую неделю',24),(46,'Какое расписание на этой неделе',24),(47,'Расписание на следующую неделю',25),(48,'Какое расписание на следующую неделю',25),(49,'Мое расписание на следующую неделю',25),(50,'Расписание занятий',26),(51,'расписание',26),(52,'На сегодня',27),(53,'Сегодня',27),(54,'На этой неделе',28),(55,'Эта неделя',28),(56,'текущая неделя',28),(57,'На текущую неделю',28),(58,'Следующая неделя',29),(59,'На следующую неделю',29),(60,'Что нового?',30),(61,'Какие последние новости',30),(62,'Аудитория свободна?',31),(63,'аудитория свободна на день пару',32),(64,'Свободна ли аудитория сейчас?',31),(65,'Аудитория свободна сейчас?',31);
/*!40000 ALTER TABLE `questiontab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-25 20:44:15
