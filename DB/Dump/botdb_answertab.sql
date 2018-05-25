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
-- Table structure for table `answertab`
--

DROP TABLE IF EXISTS `answertab`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answertab` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `answer` varchar(255) DEFAULT NULL,
  `idContext` int(11) NOT NULL,
  `idAction` int(11) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `answertab`
--

LOCK TABLES `answertab` WRITE;
/*!40000 ALTER TABLE `answertab` DISABLE KEYS */;
INSERT INTO `answertab` VALUES (12,'Приветствую',10,1),(13,'Здравствуйте!',10,1),(14,'Салют!',10,1),(15,'Хорошо',11,1),(16,'Все в пределах нормы',11,1),(17,'Принимаю ваши сообщения',12,1),(18,'Ожидаю вашего следующего вопроса',12,1),(19,'Текущее время :',13,4),(20,'Запускаю тестовое действие: ',14,5),(21,'Запускаю проверочный скрипт',15,6),(22,'Проверка скрипта',15,6),(23,'Режим беседы активирован. Чтобы вернуться в стандартный режим введите команду ЗАКОНЧИТЬ_БЕСЕДУ.',16,7),(24,'Я интеллектуальная диалоговая система.',17,1),(25,'Дайте подумать...',18,8),(26,'Запрашиваю таблицу расписания на сегодня ...',19,9),(27,'Сейчас посмотрю ...',20,10),(33,'Проверяю ваше расписание на этой неделе ...',24,12),(34,'Проверяю ваше расписание на следующую неделю',25,13),(35,'Вы хотите получить расписание на сегодня, на эту неделю или на следующую неделю?',26,1),(36,'Ищу ваше расписание занятий на сегодня ...',27,9),(37,'Ищу ваше расписание на этой неделе ...',28,12),(38,'Ищу ваше расписание на слудеющую неделю ...',29,13),(39,'Проверяю последние новости.',30,14),(40,'Проверяю запрашиваемую аудиторию ...',31,15),(41,'Запрашиваю информацию о аудитории на указанную пару.',32,16);
/*!40000 ALTER TABLE `answertab` ENABLE KEYS */;
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
