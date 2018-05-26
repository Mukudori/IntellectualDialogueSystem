-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: riidb
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
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fio` varchar(45) DEFAULT NULL,
  `idClientGroup` int(11) DEFAULT NULL,
  `idInfo` int(11) DEFAULT NULL,
  `shortfio` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (1,'Шпаков Владислав',3,1,'Шпаков В.'),(2,'Ларина Нина Александровна',2,1,'Ларина Н.А.'),(3,'Никитенко Евгений Витальевич',2,2,'Никитенко Е.В.'),(4,'Скоробогатов Михаил Сергеевич',2,3,'Скоробогатов М.С.'),(13,'Дудник Евгения Александровна',2,14,'Дудник Е.А.'),(22,'Попова Людмила Анатольевна',2,19,'Попова Л.А.'),(23,'Обухова Галина Александровна',2,21,'Обухова Г.А.'),(24,'Ястребов Геннадий Юрьевич	',2,22,'Ястребов Г.Ю.'),(25,'Михайленко Олег Анатольевич',2,23,'Михайленко О.А.'),(26,'Гриценко Вячеслав Владимирович',2,24,'Гриценко В.В.'),(27,'Гончаров Сергей Алексеевич',2,25,'Гончаров С.А.'),(28,'Павлов Александр Юрьевич',2,26,'Павлов А.Ю.'),(29,'Осадчая Ольга Петровна	',2,27,'Осадчая О.П.'),(30,'Ксендзов Владимир Олегович',2,28,'Ксендзов В.О.'),(31,'Асканова Оксана Владимировна',2,29,'Асканова О.В.'),(32,'Тест ИВТ-51',3,2,''),(33,'Артемьев Владислав',3,1,'Артемьев В'),(34,'Кожевятов Михаил',3,1,'Кожевятов М.'),(35,'Копылова Оксана',3,1,'Копылова О.'),(36,'Кяшкина Аннастасия',3,1,'Яшкина А.'),(37,'Коротаев Николай',3,1,'Коротаев Н.'),(38,'Сапожков Максим',3,1,'Сапожков М.'),(39,'Манасян Абел',3,1,'Манасян А.'),(40,'Зорина Наталья Сергеевна',2,30,'Зорина Н.С.'),(41,'Обухович Татьяна Михайловна',2,31,'Обухович Т.М.'),(42,'Рассказова Наталья Владимировна',2,32,'Рассказова Н.В.'),(43,'Шульман Ирина Борисовна',2,33,'Шульман И.Б.');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-26 21:31:57
