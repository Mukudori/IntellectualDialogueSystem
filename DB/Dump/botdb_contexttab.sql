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
-- Table structure for table `contexttab`
--

DROP TABLE IF EXISTS `contexttab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contexttab` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `header` varchar(45) NOT NULL,
  `idParent` int(11) DEFAULT '0',
  `level` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contexttab`
--

LOCK TABLES `contexttab` WRITE;
/*!40000 ALTER TABLE `contexttab` DISABLE KEYS */;
INSERT INTO `contexttab` VALUES (10,'Приветствие',0,0),(11,'Приветствие >> Как дела',10,1),(12,'Приветствие >> Как дела >> Что делаешь',11,2),(13,'Запрос текущего времени',0,0),(14,'Тест',0,0),(15,'Проверочный контекст',0,0),(16,'Активация режима ИИ',0,0),(17,'Информация о системе',0,0),(18,'Кто я?',0,0),(19,'Запрос расписания на день',0,0),(20,'Какая сейчас неделя',0,0),(24,'Запрос расписания на текущую неделю',0,0),(25,'Расписание на следующую неделю',0,0),(26,'Уточнения расписания',0,0),(27,'Уточнения расписания >> Сегодня',26,1),(28,'Уточнения расписания >> На этой неделе',26,1),(29,'Уточнения расписания >> Следующая неделя',26,1),(30,'Запрос последних новостей',0,0),(31,'Проверка свободной аудитории',0,0),(32,'Проверка сободной аудитории на день, пару',0,0),(33,'Список проекторов',0,0),(34,'Список проекторов >> Резервирование проектора',33,1),(35,'Сдача проектора на кафедру',0,0),(36,'Что ты умеешь?',0,0);
/*!40000 ALTER TABLE `contexttab` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-26 21:31:56
