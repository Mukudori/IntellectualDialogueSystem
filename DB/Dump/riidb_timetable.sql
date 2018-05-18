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
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timetable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `discipline` varchar(45) DEFAULT NULL,
  `idTeacher` int(11) DEFAULT NULL,
  `idCathGroup` int(11) DEFAULT NULL,
  `numDay` int(11) DEFAULT NULL,
  `numLesson` int(11) DEFAULT NULL,
  `idAud` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES (8,'Метрология',40,2,1,2,55),(14,'ТЕСТ',4,2,1,1,1),(17,'КТО (лек)',2,1,1,1,161),(18,'Защита информации (лек)',2,1,1,2,59),(19,'Архитектура ЭВМ (лек)',4,1,1,3,90),(21,'Защита информации (лек)',2,1,2,2,59),(22,'Функц. анализ (лек)',3,1,2,3,88),(23,'Функц. анализ (прак)',3,1,2,4,88),(24,'Мат.моделирование (лам)',2,1,3,1,135),(25,'Мат.моделирование (лаб)',2,1,3,2,135),(26,'Защита информации (лаб)',2,1,3,3,134),(27,'Функц. анализ (прак)',3,1,4,1,90),(28,'Функц. анализ (прак)',3,1,4,2,90),(29,'Интеллект. системы (лек)',4,1,4,3,59),(30,'Интеллект. системы (лаб)',4,1,5,2,135),(31,'Интеллект. системы',4,1,5,3,90),(32,'Архитектура ЭВМ (прак)',4,1,7,1,135),(33,'Архитектура ЭВМ (лек)',4,1,7,2,90),(34,'Функц. анализ',3,1,8,1,89),(35,'Функц. анализ (лек)',3,1,8,2,89),(36,'Интеллект. системы (лек)',4,1,8,3,90),(37,'Мат. Маделирование (лаб)',2,1,9,2,135),(38,'Защита информации (лаб)',2,1,9,3,135),(39,'КТО (лаб)',2,1,10,2,135),(40,'Защита информации (лек)',2,1,10,3,162),(41,'КТО (лаб)',2,1,10,4,135),(42,'КТО (лек)',2,1,11,1,59),(43,'Архитектура ЭВМ (лек)',4,1,11,2,59),(44,'КТО (лек)',2,1,11,3,59),(45,'Мат.моделирование (лек)',2,1,12,2,117),(46,'Мат.моделирование',2,1,12,3,117),(47,'Мат.моделирование',2,1,12,4,117),(48,'Доп. главы',2,2,1,3,162);
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-18 20:35:07
