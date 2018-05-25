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
-- Table structure for table `teacherinfo`
--

DROP TABLE IF EXISTS `teacherinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `teacherinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dolzhnost` varchar(100) DEFAULT NULL,
  `obrazovanie` varchar(100) DEFAULT NULL,
  `stepen` varchar(100) DEFAULT NULL,
  `zvanie` varchar(100) DEFAULT NULL,
  `kvalifikacia` varchar(100) DEFAULT NULL,
  `idCath` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacherinfo`
--

LOCK TABLES `teacherinfo` WRITE;
/*!40000 ALTER TABLE `teacherinfo` DISABLE KEYS */;
INSERT INTO `teacherinfo` VALUES (1,'доцент','высшее профессиональное','кандидат педагогических наук','доцент','Учитель средней школы',1),(2,'доцент','высшее профессиональное','кандидат физико-математических наук','доцент','Математик',1),(3,'-','-','-','-','-',1),(14,'заведующий кафедрой','высшее профессиональное','кандидат физико-математических наук','доцент','Механик. Прикладная математика',1),(19,'доцент','высшее профессиональное','кандидат физико-математических наук','-','Учитель математики, информатики и вычислительной техники средней школы',1),(20,'','','','','',1),(21,'заведующий кафедрой','высшее профессиональное','кандидат физико-математичес-ких наук','доцент','Математик',26),(22,'заведующий кафедрой	','высшее профессиональное','кандидат технических наук','доцент','Инженер-механик',27),(23,'и.о.заведующего кафедрой','высшее профессиональное	','кандидат технических наук','-','Инженер',28),(24,'заведующий кафедрой','высшее профессиональное','кандидат технических наук','доцент','Инженер-механик',29),(25,'заведующий кафедрой','высшее профессиональное','кандидат технических наук','доцент','Инженер-физик',30),(26,'заведующий кафедрой','высшее профессиональное','кандидат философ-ских наук','доцент','Инженер-механик	',31),(27,'заведующий кафедрой','высшее профессиональное','доктор экономичес-ких наук','доцент','Инженер-экономист связи',32),(28,'заведующий кафедрой','высшее профессиональное','кандидат технических наук','доцент','Инженер-механик',33),(29,'заведующий кафедрой','высшее профессиональное','доктор экономических наук','доцент','Экономист',34),(30,'доцент','высшее профессиональное','кандидат педагогических наук','-','Инженер-математик',1),(31,'старший преподаватель','высшее профессиональное','-','-','Математик',1),(32,'старший преподаватель','высшее профессиональное','-','-','Математик',1),(33,'доцент','высшее профессиональное','кандидат технических наук	','-','Учитель математики и информатики',1);
/*!40000 ALTER TABLE `teacherinfo` ENABLE KEYS */;
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
