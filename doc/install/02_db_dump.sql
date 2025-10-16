CREATE DATABASE  IF NOT EXISTS `tooltoucan` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `tooltoucan`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: drago    Database: tooltoucan
-- ------------------------------------------------------
-- Server version	8.0.42-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `HTMLTarget`
--

DROP TABLE IF EXISTS `HTMLTarget`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `HTMLTarget` (
  `idHtmlTarget` int NOT NULL AUTO_INCREMENT,
  `htText` varchar(45) NOT NULL,
  `htValue` varchar(45) NOT NULL,
  PRIMARY KEY (`idHtmlTarget`),
  UNIQUE KEY `dText_UNIQUE` (`htText`),
  UNIQUE KEY `dValue_UNIQUE` (`htValue`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `HTMLTarget`
--

LOCK TABLES `HTMLTarget` WRITE;
/*!40000 ALTER TABLE `HTMLTarget` DISABLE KEYS */;
INSERT INTO `HTMLTarget` VALUES (1,'This Page','_SELF'),(2,'New Page','_blank'),(3,'Embedded','tt_embedded');
/*!40000 ALTER TABLE `HTMLTarget` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Link`
--

DROP TABLE IF EXISTS `Link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Link` (
  `idLink` int NOT NULL AUTO_INCREMENT,
  `lName` varchar(45) NOT NULL,
  `lURI` varchar(2048) NOT NULL,
  `lcId` int NOT NULL,
  `lGroup` varchar(45) DEFAULT NULL,
  `lDescription` varchar(255) DEFAULT NULL,
  `lRank` int DEFAULT NULL,
  `htId` int NOT NULL,
  `lPreset` varchar(20) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`idLink`),
  KEY `fkLinkCategory_idx` (`lcId`),
  KEY `fkDestination_idx` (`htId`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `LinkCategory`
--

DROP TABLE IF EXISTS `LinkCategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `LinkCategory` (
  `idLinkCategory` int NOT NULL AUTO_INCREMENT,
  `lcName` varchar(45) NOT NULL,
  `lcDescription` varchar(255) DEFAULT NULL,
  `lcRank` int DEFAULT NULL,
  `lPreset` varchar(20) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`idLinkCategory`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary view structure for view `nav_view`
--

DROP TABLE IF EXISTS `nav_view`;
/*!50001 DROP VIEW IF EXISTS `nav_view`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `nav_view` AS SELECT 
 1 AS `idLink`,
 1 AS `lcId`,
 1 AS `lcName`,
 1 AS `lGroup`,
 1 AS `lName`,
 1 AS `htValue`,
 1 AS `lURI`,
 1 AS `lDescription`,
 1 AS `lcDescription`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `nav_view`
--

/*!50001 DROP VIEW IF EXISTS `nav_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `nav_view` AS select `Link`.`idLink` AS `idLink`,`Link`.`lcId` AS `lcId`,`LinkCategory`.`lcName` AS `lcName`,`Link`.`lGroup` AS `lGroup`,`Link`.`lName` AS `lName`,`HTMLTarget`.`htValue` AS `htValue`,`Link`.`lURI` AS `lURI`,`Link`.`lDescription` AS `lDescription`,`LinkCategory`.`lcDescription` AS `lcDescription` from ((`Link` join `LinkCategory` on((`Link`.`lcId` = `LinkCategory`.`idLinkCategory`))) join `HTMLTarget` on((`Link`.`htId` = `HTMLTarget`.`idHtmlTarget`))) order by `LinkCategory`.`lcRank`,`Link`.`lRank`,`LinkCategory`.`lcName`,trim(`Link`.`lGroup`),`Link`.`lName` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-16 15:53:41
