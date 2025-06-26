CREATE DATABASE  IF NOT EXISTS `testdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `testdb`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: testdb
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT '0',
  `status` varchar(50) DEFAULT NULL,
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,53,99,'Used in Service','2025-06-26 22:30:56'),(2,54,99,'Used in Service','2025-06-26 22:30:56'),(3,55,49,'Used in Service','2025-06-26 22:30:56');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_status`
--

DROP TABLE IF EXISTS `inventory_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_status` (
  `inventory_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `status` enum('In Stock','Low Stock','Out of Stock','Received','Updated') NOT NULL DEFAULT 'In Stock',
  `supplier_name` varchar(255) DEFAULT NULL,
  `last_updated` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`inventory_id`),
  UNIQUE KEY `unique_product` (`product_id`),
  CONSTRAINT `inventory_status_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_status`
--

LOCK TABLES `inventory_status` WRITE;
/*!40000 ALTER TABLE `inventory_status` DISABLE KEYS */;
INSERT INTO `inventory_status` VALUES (1,1,'Neocell - 360',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(2,2,'Hydrocort',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(3,3,'Underarm Set',30,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(4,4,'Clear Set Whitening Set',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(5,5,'Acne Set',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(6,6,'Breakout Set',35,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(7,7,'Warts Set',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(8,8,'Melasma Set',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(9,9,'Niacinamide Set',30,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(10,10,'Rejuv Set',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(11,11,'Gluta Lotion Tomato',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(12,12,'Glutathione Lotion',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(13,13,'Bleaching Lotion',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(14,14,'Whipped Scrub',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(15,15,'Gluta Liquid Soap',70,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(16,16,'Instawhite Lotion',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(17,17,'Collagen Serum',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(18,18,'Vitamin C & E Serum',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(19,19,'Niacinamide Serum',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(20,20,'Underarm Toner',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(21,21,'Underarm Liquid Gluta Soap',70,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(22,22,'Underarm Whitening Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(23,23,'Underarm Deo Whitening Spray',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(24,24,'BAR SOAP - NIACINAMIDE',80,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(25,25,'BAR SOAP - COLLAGEN',80,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(26,26,'BAR SOAP - PAPAYA',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(27,27,'BAR SOAP - KOJIC',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(28,28,'BAR SOAP - GLUTA KOJIC',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(29,29,'BAR SOAP - OATMEAL SOAP',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(30,30,'Moisturizing Soap',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(31,31,'Clear Set Clarifying Toner No1',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(32,32,'Clear Set Whitening Toner No2',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(33,33,'Clear Set Night Cream 4',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(34,34,'Clear Set Night Cream 5',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(35,35,'Clear Set Sunblock',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(36,36,'Oatmeal Soap',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(37,37,'Melasma Toner',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(38,38,'Melasma Medicated Toner',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(39,39,'Melasma Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(40,40,'Melasma Bleaching Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(41,41,'Melasma Sunblock',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(42,42,'Niacinamide Aloe Vera Cleansing Soap',80,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(43,43,'Niacinamide Sunblock',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(44,44,'Niacinamide Clarifying Toner',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(45,45,'Niacinamide Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(46,46,'Breakout Acne Facial Wash',70,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(47,47,'Breakout Sun Protect Gel',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(48,48,'Breakout Brightening Serum',40,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(49,49,'Breakout Acne Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(50,50,'Acne Quick Dry Solution',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(51,51,'Acne Tea Tree Liquid Soap',70,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(52,52,'Acne Cream',60,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(53,53,'Nail Polish',99,'In Stock',NULL,'2025-06-27 06:30:56','2025-06-26 22:19:52'),(54,54,'UV Gel Polish',99,'In Stock',NULL,'2025-06-27 06:30:56','2025-06-26 22:19:52'),(55,55,'Nail Extension Material',49,'In Stock',NULL,'2025-06-27 06:30:56','2025-06-26 22:19:52'),(56,56,'Eyelash Extension Adhesive',80,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(57,57,'Synthetic Lashes',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(58,58,'Facial Cleanser',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(59,59,'Chemical Peel Solution',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(60,60,'Waxing Strips',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(61,61,'Waxing Solution',100,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(62,62,'Permanent Makeup Pigments',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(63,63,'BB Glow Pigments',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(64,64,'Glutathione IV Solution',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52'),(65,65,'Collagen IV Solution',50,'In Stock',NULL,'2025-06-27 06:19:52','2025-06-26 22:19:52');
/*!40000 ALTER TABLE `inventory_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_transactions`
--

DROP TABLE IF EXISTS `inventory_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `transaction_type` enum('Stock In','Stock Out','Adjustment') NOT NULL,
  `quantity` int NOT NULL,
  `notes` text,
  `transaction_date` datetime NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_transactions`
--

LOCK TABLES `inventory_transactions` WRITE;
/*!40000 ALTER TABLE `inventory_transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `product_name` varchar(255) NOT NULL,
  `description` text,
  `category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int DEFAULT '0',
  `threshold_value` int DEFAULT '10',
  `expiry_date` date DEFAULT NULL,
  `icon` varchar(255) DEFAULT NULL,
  `availability` tinyint(1) DEFAULT '1',
  `status` varchar(50) DEFAULT 'In Stock',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Neocell - 360','A comprehensive skin supplement to promote collagen production and overall skin health.','SKIN CARE PRODUCTS',2500.00,50,20,'2026-06-27','/icons/neocell_360.png',1,'Active'),(2,'Hydrocort','A hydrocortisone-based cream to reduce inflammation and soothe irritated skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/hydrocort.png',1,'Active'),(3,'Underarm Set','A complete underarm care kit for whitening and smoothening the underarm area.','SKIN CARE PRODUCTS',700.00,30,20,'2026-06-27','/icons/underarm_set.png',1,'Active'),(4,'Clear Set Whitening Set','A skincare set designed to brighten and even out skin tone for a radiant complexion.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/clear_set_whitening.png',1,'Active'),(5,'Acne Set','A targeted skincare set to treat and prevent acne, including cleansing and treatment products.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/acne_set.png',1,'Active'),(6,'Breakout Set','A specialized set to address acne breakouts and promote clearer, healthier skin.','SKIN CARE PRODUCTS',1800.00,35,20,'2026-06-27','/icons/breakout_set.png',1,'Active'),(7,'Warts Set','A treatment kit designed to target and reduce the appearance of warts.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/warts_set.png',1,'Active'),(8,'Melasma Set','A skincare set formulated to reduce melasma and hyperpigmentation for even-toned skin.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/melasma_set.png',1,'Active'),(9,'Niacinamide Set','A complete niacinamide-based skincare set to brighten skin and minimize pores.','SKIN CARE PRODUCTS',2500.00,30,20,'2026-06-27','/icons/niacinamide_set.png',1,'Active'),(10,'Rejuv Set','A rejuvenating skincare set to hydrate and revitalize the skin for a youthful glow.','SKIN CARE PRODUCTS',600.00,50,20,'2026-06-27','/icons/rejuv_set.png',1,'Active'),(11,'Gluta Lotion Tomato','A glutathione and tomato-infused lotion for skin brightening and hydration.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/gluta_lotion_tomato.png',1,'Active'),(12,'Glutathione Lotion','A lotion with glutathione to promote skin whitening and a smoother complexion.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/glutathione_lotion.png',1,'Active'),(13,'Bleaching Lotion','A skin-lightening lotion to reduce dark spots and even out skin tone.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/bleaching_lotion.png',1,'Active'),(14,'Whipped Scrub','A whipped exfoliating scrub to remove dead skin and promote a smooth, radiant complexion.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/whipped_scrub.png',1,'Active'),(15,'Gluta Liquid Soap','A liquid soap infused with glutathione for gentle cleansing and skin brightening.','SKIN CARE PRODUCTS',300.00,70,20,'2026-06-27','/icons/gluta_liquid_soap.png',1,'Active'),(16,'Instawhite Lotion','A fast-acting whitening lotion to brighten and hydrate the skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/instawhite_lotion.png',1,'Active'),(17,'Collagen Serum','A collagen-infused serum to improve skin elasticity and reduce signs of aging.','SKIN CARE PRODUCTS',1000.00,40,20,'2026-06-27','/icons/collagen_serum.png',1,'Active'),(18,'Vitamin C & E Serum','A serum with vitamins C and E to brighten skin and protect against environmental damage.','SKIN CARE PRODUCTS',850.00,50,20,'2026-06-27','/icons/vitamin_c_e_serum.png',1,'Active'),(19,'Niacinamide Serum','A niacinamide serum to minimize pores, reduce redness, and enhance skin clarity.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/niacinamide_serum.png',1,'Active'),(20,'Underarm Toner','A toner designed to brighten and smooth the underarm area.','SKIN CARE PRODUCTS',400.00,50,20,'2026-06-27','/icons/underarm_toner.png',1,'Active'),(21,'Underarm Liquid Gluta Soap','A liquid soap with glutathione for cleansing and whitening the underarm area.','SKIN CARE PRODUCTS',150.00,70,20,'2026-06-27','/icons/underarm_gluta_soap.png',1,'Active'),(22,'Underarm Whitening Cream','A cream formulated to lighten and soften underarm skin.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/underarm_whitening_cream.png',1,'Active'),(23,'Underarm Deo Whitening Spray','A deodorizing spray with whitening properties for underarm care.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/underarm_deo_spray.png',1,'Active'),(24,'BAR SOAP - NIACINAMIDE','A niacinamide-infused bar soap for cleansing and brightening the skin.','SKIN CARE PRODUCTS',250.00,80,20,'2026-06-27','/icons/bar_soap_niacinamide.png',1,'Active'),(25,'BAR SOAP - COLLAGEN','A collagen-enriched bar soap to hydrate and improve skin elasticity.','SKIN CARE PRODUCTS',250.00,80,20,'2026-06-27','/icons/bar_soap_collagen.png',1,'Active'),(26,'BAR SOAP - PAPAYA','A papaya-based bar soap for gentle exfoliation and skin brightening.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_papaya.png',1,'Active'),(27,'BAR SOAP - KOJIC','A kojic acid bar soap to reduce dark spots and promote even skin tone.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_kojic.png',1,'Active'),(28,'BAR SOAP - GLUTA KOJIC','A bar soap with glutathione and kojic acid for enhanced skin whitening and cleansing.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_gluta_kojic.png',1,'Active'),(29,'BAR SOAP - OATMEAL SOAP','An oatmeal bar soap for gentle exfoliation and soothing sensitive skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_oatmeal.png',1,'Active'),(30,'Moisturizing Soap','A hydrating soap to cleanse and moisturize the skin, leaving it soft and smooth.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/moisturizing_soap.png',1,'Active'),(31,'Clear Set Clarifying Toner No1','A clarifying toner from the Clear Set to cleanse and prepare skin for further treatment.','SKIN CARE PRODUCTS',350.00,50,20,'2026-06-27','/icons/clear_set_toner_no1.png',1,'Active'),(32,'Clear Set Whitening Toner No2','A whitening toner from the Clear Set to brighten and even out skin tone.','SKIN CARE PRODUCTS',400.00,50,20,'2026-06-27','/icons/clear_set_toner_no2.png',1,'Active'),(33,'Clear Set Night Cream 4','A night cream from the Clear Set to hydrate and repair skin overnight.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_night_cream_4.png',1,'Active'),(34,'Clear Set Night Cream 5','An advanced night cream from the Clear Set for intensive skin nourishment.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_night_cream_5.png',1,'Active'),(35,'Clear Set Sunblock','A sunblock from the Clear Set to protect skin from UV damage.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_sunblock.png',1,'Active'),(36,'Oatmeal Soap','An oatmeal-based soap for gentle cleansing and soothing irritated or sensitive skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/oatmeal_soap.png',1,'Active'),(37,'Melasma Toner','A toner formulated to reduce melasma and hyperpigmentation for clearer skin.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/melasma_toner.png',1,'Active'),(38,'Melasma Medicated Toner','A medicated toner to target melasma and even out skin tone.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_medicated_toner.png',1,'Active'),(39,'Melasma Cream','A cream designed to treat melasma and reduce dark spots.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_cream.png',1,'Active'),(40,'Melasma Bleaching Cream','A bleaching cream to lighten melasma and promote an even complexion.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_bleaching_cream.png',1,'Active'),(41,'Melasma Sunblock','A sunblock formulated to protect skin with melasma from UV damage.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/melasma_sunblock.png',1,'Active'),(42,'Niacinamide Aloe Vera Cleansing Soap','A cleansing soap with niacinamide and aloe vera to brighten and soothe skin.','SKIN CARE PRODUCTS',200.00,80,20,'2026-06-27','/icons/niacinamide_aloe_soap.png',1,'Active'),(43,'Niacinamide Sunblock','A niacinamide-infused sunblock to protect and brighten skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/niacinamide_sunblock.png',1,'Active'),(44,'Niacinamide Clarifying Toner','A clarifying toner with niacinamide to reduce redness and refine pores.','SKIN CARE PRODUCTS',600.00,50,20,'2026-06-27','/icons/niacinamide_clarifying_toner.png',1,'Active'),(45,'Niacinamide Cream','A niacinamide cream to hydrate and improve skin clarity and texture.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/niacinamide_cream.png',1,'Active'),(46,'Breakout Acne Facial Wash','A facial wash from the Breakout Set to cleanse and treat acne-prone skin.','SKIN CARE PRODUCTS',300.00,70,20,'2026-06-27','/icons/breakout_acne_wash.png',1,'Active'),(47,'Breakout Sun Protect Gel','A sun protection gel from the Breakout Set for acne-prone skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/breakout_sun_protect_gel.png',1,'Active'),(48,'Breakout Brightening Serum','A brightening serum from the Breakout Set to reduce acne marks and enhance skin clarity.','SKIN CARE PRODUCTS',900.00,40,20,'2026-06-27','/icons/breakout_brightening_serum.png',1,'Active'),(49,'Breakout Acne Cream','An acne cream from the Breakout Set to treat and prevent breakouts.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/breakout_acne_cream.png',1,'Active'),(50,'Acne Quick Dry Solution','A fast-acting solution to dry out and treat active acne spots.','SKIN CARE PRODUCTS',700.00,50,20,'2026-06-27','/icons/acne_quick_dry_solution.png',1,'Active'),(51,'Acne Tea Tree Liquid Soap','A tea tree-infused liquid soap to cleanse and soothe acne-prone skin.','SKIN CARE PRODUCTS',200.00,70,20,'2026-06-27','/icons/acne_tea_tree_soap.png',1,'Active'),(52,'Acne Cream','A targeted cream to reduce acne and promote clearer skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/acne_cream.png',1,'Active'),(53,'Nail Polish','Standard nail polish used in manicure and pedicure services.','NAIL CARE',10.00,99,15,'2026-06-27','/icons/nail_polish.png',1,'Active'),(54,'UV Gel Polish','UV-curable gel polish for long-lasting manicures and pedicures.','NAIL CARE',20.00,99,15,'2026-06-27','/icons/uv_gel_polish.png',1,'Active'),(55,'Nail Extension Material','Materials for applying nail extensions, including acrylic or gel.','NAIL CARE',50.00,49,15,'2026-06-27','/icons/nail_extension_material.png',1,'Active'),(56,'Eyelash Extension Adhesive','Adhesive used for applying eyelash extensions.','BROWS & LASHES',30.00,80,15,'2026-06-27','/icons/eyelash_adhesive.png',1,'Active'),(57,'Synthetic Lashes','Synthetic lashes for classic and volume eyelash extension services.','BROWS & LASHES',25.00,100,15,'2026-06-27','/icons/synthetic_lashes.png',1,'Active'),(58,'Facial Cleanser','Cleanser used in facial treatments for cleansing and preparation.','FACE & BODY',15.00,50,15,'2026-06-27','/icons/facial_cleanser.png',1,'Active'),(59,'Chemical Peel Solution','Solution used for chemical peel facials to exfoliate and renew skin.','FACE & BODY',40.00,50,15,'2026-06-27','/icons/chemical_peel_solution.png',1,'Active'),(60,'Waxing Strips','Strips used for waxing services to remove hair.','WAXING',10.00,100,15,'2026-06-27','/icons/waxing_strips.png',1,'Active'),(61,'Waxing Solution','Wax solution used for hair removal in waxing services.','WAXING',15.00,100,15,'2026-06-27','/icons/waxing_solution.png',1,'Active'),(62,'Permanent Makeup Pigments','Pigments used for microshading, microblading, and eyeliner services.','PERMANENT MAKEUP',30.00,50,15,'2026-06-27','/icons/permanent_makeup_pigments.png',1,'Active'),(63,'BB Glow Pigments','Pigments used for Korean BB Glow treatments for semi-permanent makeup.','PERMANENT MAKEUP',35.00,50,15,'2026-06-27','/icons/bb_glow_pigments.png',1,'Active'),(64,'Glutathione IV Solution','IV solution used for glutathione drip and push treatments.','GLUTATHIONE',50.00,50,15,'2026-03-27','/icons/glutathione_iv_solution.png',1,'Active'),(65,'Collagen IV Solution','IV solution used for collagen push treatments.','GLUTATHIONE',50.00,50,15,'2026-03-27','/icons/collagen_iv_solution.png',1,'Active');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service_products`
--

DROP TABLE IF EXISTS `service_products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service_products` (
  `service_product_id` int NOT NULL AUTO_INCREMENT,
  `service_id` int NOT NULL,
  `product_id` int NOT NULL,
  `quantity` int DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`service_product_id`),
  KEY `service_id` (`service_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `service_products_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`) ON DELETE CASCADE,
  CONSTRAINT `service_products_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_products`
--

LOCK TABLES `service_products` WRITE;
/*!40000 ALTER TABLE `service_products` DISABLE KEYS */;
INSERT INTO `service_products` VALUES (1,1,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(2,2,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(3,3,53,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(4,4,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(5,5,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(6,6,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(7,7,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(8,8,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(9,9,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(10,10,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(11,11,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(12,12,53,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(13,13,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(14,14,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(15,15,53,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(16,16,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(17,17,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(18,18,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(19,19,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(20,20,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(21,21,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(22,22,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(23,23,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(24,24,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(25,25,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(26,26,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(27,27,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(28,28,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(29,31,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(30,31,57,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(31,32,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(32,32,57,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(33,33,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(34,33,57,3,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(35,34,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(36,35,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(37,36,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(38,37,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(39,37,46,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(40,38,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00');
/*!40000 ALTER TABLE `service_products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `services`
--

DROP TABLE IF EXISTS `services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `services` (
  `service_id` int NOT NULL AUTO_INCREMENT,
  `service_name` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `availability` tinyint(1) DEFAULT '1',
  `description` text,
  PRIMARY KEY (`service_id`)
) ENGINE=InnoDB AUTO_INCREMENT=112 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Basic Manicure','NAIL CARE',90.00,1,'is a nail treatment that includes shaping and filing the nails'),(2,'Basic Pedicure','NAIL CARE',120.00,1,'is a cosmetic foot and nail treatment focused on grooming and enhancing the appearance of the feet and toenails.'),(3,'Basic Duo','NAIL CARE',180.00,1,'combination of manicure and pedicure'),(4,'Classic Eyelash Extension','BROWS & LASHES',600.00,1,'Application of individual synthetic lashes to each natural lash for a natural, enhanced look.'),(5,'Volume Eyelash Extension','BROWS & LASHES',1200.00,1,'Application of multiple lightweight synthetic lashes per natural lash for a fuller, dramatic effect.'),(6,'Russian Volume Eyelash Extension','BROWS & LASHES',1500.00,1,'Advanced technique applying ultra-fine synthetic lashes in a fan-like structure for maximum volume and density.'),(7,'Dermabrasion (Diamond) Whitening Facial','FACE & BODY',800.00,1,'A diamond-tip microdermabrasion facial that exfoliates and brightens skin for a radiant complexion.'),(8,'Hydrafacial','FACE & BODY',1500.00,1,'A non-invasive facial treatment that cleanses, exfoliates, extracts, and hydrates for glowing skin.'),(9,'Rf Contouring Facial','FACE & BODY',1000.00,1,'A radiofrequency facial that tightens and contours skin, promoting collagen production for a youthful look.'),(10,'Acne Facial Treatment','FACE & BODY',1500.00,1,'A specialized facial targeting acne, including deep cleansing, exfoliation, and soothing treatments.'),(11,'Non Invasive Botox Facial','FACE & BODY',1800.00,1,'A non-invasive facial using advanced techniques to reduce fine lines and mimic Botox effects.'),(12,'2 Hour Miracle Facial','FACE & BODY',2500.00,1,'An intensive 2-hour facial combining multiple techniques for deep hydration, lifting, and rejuvenation.'),(13,'Anti Aging Miracle Facial','FACE & BODY',1800.00,1,'A facial focused on reducing signs of aging, with targeted treatments for wrinkles and firmness.'),(14,'Black Doll Facial','FACE & BODY',1500.00,1,'A carbon laser facial that reduces pigmentation, refines pores, and promotes a smoother complexion.'),(15,'Deep Facial Chemical Peel','FACE & BODY',2500.00,1,'A deep chemical peel to exfoliate and renew skin, addressing fine lines, scars, and uneven tone.'),(16,'Underarm Whitening (10 Sessions W After Care Kit)','FACE & BODY',10000.00,1,'A 10-session underarm whitening treatment with an aftercare kit to lighten and smooth skin.'),(17,'Underarm Black Doll Whitening (10 Sessions)','FACE & BODY',6000.00,1,'A 10-session underarm whitening treatment using Black Doll laser technology for effective lightening.'),(18,'Microshading (2 Sessions)','PERMANENT MAKEUP',2500.00,1,'A 2-session microshading procedure to create soft, powdered brows with a natural, filled-in look.'),(19,'Combrows (Microblading & Microshading 2 Sessions)','PERMANENT MAKEUP',3500.00,1,'A 2-session combination of microblading and microshading for defined, natural-looking brows with added depth.'),(20,'Classic Eyeliner (2 Sessions)','PERMANENT MAKEUP',1500.00,1,'A 2-session permanent makeup treatment applying classic eyeliner for a subtle, defined eye look.'),(21,'Dusty Winged Eyeliner (2 Sessions)','PERMANENT MAKEUP',2500.00,1,'A 2-session permanent makeup treatment creating a soft, winged eyeliner effect for a dramatic look.'),(22,'Lip Blush (2 Sessions)','PERMANENT MAKEUP',3000.00,1,'A 2-session lip blush treatment to enhance lip color and shape with a natural, semi-permanent tint.'),(23,'Korean BB Glow Foundation W Classic Facial','PERMANENT MAKEUP',1500.00,1,'A single-session Korean BB Glow treatment with a classic facial, applying semi-permanent foundation for even skin tone.'),(24,'5+1 Korean BB Glow Foundation W Classic Facial','PERMANENT MAKEUP',7500.00,1,'A 6-session (5+1 free) Korean BB Glow treatment with classic facials, providing long-lasting semi-permanent foundation.'),(25,'Korean BB Glow Blush W Classic Facial','PERMANENT MAKEUP',700.00,1,'A single-session Korean BB Glow blush treatment with a classic facial, adding a semi-permanent rosy glow.'),(26,'5+1 Korean BB Glow Blush W Classic Facial','PERMANENT MAKEUP',3500.00,1,'A 6-session (5+1 free) Korean BB Glow blush treatment with classic facials, enhancing cheeks with semi-permanent color.'),(27,'Korean BB Glow Contour W Classic Facial','PERMANENT MAKEUP',1500.00,1,'A single-session Korean BB Glow contour treatment with a classic facial, adding semi-permanent contour for facial definition.'),(28,'5+1 Korean BB Glow Contour W Classic Facial','PERMANENT MAKEUP',7500.00,1,'A 6-session (5+1 free) Korean BB Glow contour treatment with classic facials, providing long-lasting semi-permanent contour.'),(29,'5+1 Dermabrasion (Diamond Whitening Facial)','VANITY PACKAGE',3500.00,1,'A 6-session (5+1 free) diamond microdermabrasion package for exfoliation and skin brightening, delivering a radiant complexion.'),(30,'5+1 Hydrafacial','VANITY PACKAGE',7000.00,1,'A 6-session (5+1 free) Hydrafacial package for deep cleansing, exfoliation, extraction, and hydration for glowing skin.'),(31,'5+1 Rf Contouring Facial','VANITY PACKAGE',5000.00,1,'A 6-session (5+1 free) radiofrequency facial package to tighten and contour skin, promoting collagen for a youthful look.'),(32,'5+1 Acne Facial Treatment','VANITY PACKAGE',7000.00,1,'A 6-session (5+1 free) acne facial package with deep cleansing, exfoliation, and soothing treatments to target acne.'),(33,'5+1 Non Invasive Botox Facial','VANITY PACKAGE',8500.00,1,'A 6-session (5+1 free) non-invasive Botox facial package to reduce fine lines and mimic Botox effects.'),(34,'5+1 2 Hour Miracle Facial','VANITY PACKAGE',12000.00,1,'A 6-session (5+1 free) 2-hour miracle facial package combining multiple techniques for deep hydration, lifting, and rejuvenation.'),(35,'Female Eyebrows Waxing','WAXING',140.00,1,'Precision waxing to shape and define female eyebrows for a clean, polished look.'),(36,'Female Upper Lip Waxing','WAXING',140.00,1,'Waxing service to remove unwanted hair from the female upper lip area.'),(37,'Female Lower Lip Waxing','WAXING',140.00,1,'Waxing to remove hair from the female lower lip area for a smooth finish.'),(38,'Female Full Face Waxing','WAXING',240.00,1,'Complete facial waxing for females, covering eyebrows, upper and lower lip, and cheeks.'),(39,'Female Underarm Waxing','WAXING',200.00,1,'Waxing service to remove hair from the female underarm area for smooth skin.'),(40,'Female Half Arm Waxing','WAXING',200.00,1,'Waxing of the lower or upper half of the female arms to remove unwanted hair.'),(41,'Female Full Arm Waxing','WAXING',300.00,1,'Full arm waxing for females, removing hair from the entire arm for a sleek appearance.'),(42,'Female Half Leg Waxing','WAXING',350.00,1,'Waxing of the lower or upper half of the female legs for smooth, hair-free skin.'),(43,'Female Full Leg Waxing','WAXING',600.00,1,'Complete leg waxing for females, removing hair from the entire leg for a polished look.'),(44,'Female Bikini Waxing','WAXING',300.00,1,'Waxing service to remove hair from the female bikini line for a clean, tidy appearance.'),(45,'Female Brazilian Waxing','WAXING',600.00,1,'Comprehensive waxing for females, removing all or most hair from the bikini area.'),(46,'Female Chest Waxing','WAXING',300.00,1,'Waxing service to remove hair from the female chest area for smooth skin.'),(47,'Female Back Torso Waxing','WAXING',350.00,1,'Waxing to remove hair from the female back torso for a clean, hair-free finish.'),(48,'Male Eyebrows Waxing','WAXING',140.00,1,'Precision waxing to shape and groom male eyebrows for a neat appearance.'),(49,'Male Upper Lip Waxing','WAXING',150.00,1,'Waxing service to remove unwanted hair from the male upper lip area.'),(50,'Neocell - 360','SKIN CARE PRODUCTS',2500.00,1,'A comprehensive skin supplement to promote collagen production and overall skin health.'),(51,'Hydrocort','SKIN CARE PRODUCTS',150.00,1,'A hydrocortisone-based cream to reduce inflammation and soothe irritated skin.'),(52,'Underarm Set','SKIN CARE PRODUCTS',700.00,1,'A complete underarm care kit for whitening and smoothening the underarm area.'),(53,'Clear Set Whitening Set','SKIN CARE PRODUCTS',1500.00,1,'A skincare set designed to brighten and even out skin tone for a radiant complexion.'),(54,'Acne Set','SKIN CARE PRODUCTS',1500.00,1,'A targeted skincare set to treat and prevent acne, including cleansing and treatment products.'),(55,'Breakout Set','SKIN CARE PRODUCTS',1800.00,1,'A specialized set to address acne breakouts and promote clearer, healthier skin.'),(56,'Warts Set','SKIN CARE PRODUCTS',500.00,1,'A treatment kit designed to target and reduce the appearance of warts.'),(57,'Melasma Set','SKIN CARE PRODUCTS',1500.00,1,'A skincare set formulated to reduce melasma and hyperpigmentation for even-toned skin.'),(58,'Niacinamide Set','SKIN CARE PRODUCTS',2500.00,1,'A complete niacinamide-based skincare set to brighten skin and minimize pores.'),(59,'Rejuv Set','SKIN CARE PRODUCTS',600.00,1,'A rejuvenating skincare set to hydrate and revitalize the skin for a youthful glow.'),(60,'Gluta Lotion Tomato','SKIN CARE PRODUCTS',300.00,1,'A glutathione and tomato-infused lotion for skin brightening and hydration.'),(61,'Glutathione Lotion','SKIN CARE PRODUCTS',300.00,1,'A lotion with glutathione to promote skin whitening and a smoother complexion.'),(62,'Bleaching Lotion','SKIN CARE PRODUCTS',300.00,1,'A skin-lightening lotion to reduce dark spots and even out skin tone.'),(63,'Whipped Scrub','SKIN CARE PRODUCTS',500.00,1,'A whipped exfoliating scrub to remove dead skin and promote a smooth, radiant complexion.'),(64,'Gluta Liquid Soap','SKIN CARE PRODUCTS',300.00,1,'A liquid soap infused with glutathione for gentle cleansing and skin brightening.'),(65,'Instawhite Lotion','SKIN CARE PRODUCTS',300.00,1,'A fast-acting whitening lotion to brighten and hydrate the skin.'),(66,'Collagen Serum','SKIN CARE PRODUCTS',1000.00,1,'A collagen-infused serum to improve skin elasticity and reduce signs of aging.'),(67,'Vitamin C & E Serum','SKIN CARE PRODUCTS',850.00,1,'A serum with vitamins C and E to brighten skin and protect against environmental damage.'),(68,'Niacinamide Serum','SKIN CARE PRODUCTS',1500.00,1,'A niacinamide serum to minimize pores, reduce redness, and enhance skin clarity.'),(69,'Underarm Toner','SKIN CARE PRODUCTS',400.00,1,'A toner designed to brighten and smooth the underarm area.'),(70,'Underarm Liquid Gluta Soap','SKIN CARE PRODUCTS',150.00,1,'A liquid soap with glutathione for cleansing and whitening the underarm area.'),(71,'Underarm Whitening Cream','SKIN CARE PRODUCTS',150.00,1,'A cream formulated to lighten and soften underarm skin.'),(72,'Underarm Deo Whitening Spray','SKIN CARE PRODUCTS',150.00,1,'A deodorizing spray with whitening properties for underarm care.'),(73,'BAR SOAP - NIACINAMIDE','SKIN CARE PRODUCTS',250.00,1,'A niacinamide-infused bar soap for cleansing and brightening the skin.'),(74,'BAR SOAP - COLLAGEN','SKIN CARE PRODUCTS',250.00,1,'A collagen-enriched bar soap to hydrate and improve skin elasticity.'),(75,'BAR SOAP - PAPAYA','SKIN CARE PRODUCTS',150.00,1,'A papaya-based bar soap for gentle exfoliation and skin brightening.'),(76,'BAR SOAP - KOJIC','SKIN CARE PRODUCTS',150.00,1,'A kojic acid bar soap to reduce dark spots and promote even skin tone.'),(77,'BAR SOAP - GLUTA KOJIC','SKIN CARE PRODUCTS',150.00,1,'A bar soap with glutathione and kojic acid for enhanced skin whitening and cleansing.'),(78,'BAR SOAP - OATMEAL SOAP','SKIN CARE PRODUCTS',150.00,1,'An oatmeal bar soap for gentle exfoliation and soothing sensitive skin.'),(79,'Moisturizing Soap','SKIN CARE PRODUCTS',150.00,1,'A hydrating soap to cleanse and moisturize the skin, leaving it soft and smooth.'),(80,'Clear Set Clarifying Toner No1','SKIN CARE PRODUCTS',350.00,1,'A clarifying toner from the Clear Set to cleanse and prepare skin for further treatment.'),(81,'Clear Set Whitening Toner No2','SKIN CARE PRODUCTS',400.00,1,'A whitening toner from the Clear Set to brighten and even out skin tone.'),(82,'Clear Set Night Cream 4','SKIN CARE PRODUCTS',150.00,1,'A night cream from the Clear Set to hydrate and repair skin overnight.'),(83,'Clear Set Night Cream 5','SKIN CARE PRODUCTS',150.00,1,'An advanced night cream from the Clear Set for intensive skin nourishment.'),(84,'Clear Set Sunblock','SKIN CARE PRODUCTS',150.00,1,'A sunblock from the Clear Set to protect skin from UV damage.'),(85,'Oatmeal Soap','SKIN CARE PRODUCTS',150.00,1,'An oatmeal-based soap for gentle cleansing and soothing irritated or sensitive skin.'),(86,'Melasma Toner','SKIN CARE PRODUCTS',500.00,1,'A toner formulated to reduce melasma and hyperpigmentation for clearer skin.'),(87,'Melasma Medicated Toner','SKIN CARE PRODUCTS',200.00,1,'A medicated toner to target melasma and even out skin tone.'),(88,'Melasma Cream','SKIN CARE PRODUCTS',200.00,1,'A cream designed to treat melasma and reduce dark spots.'),(89,'Melasma Bleaching Cream','SKIN CARE PRODUCTS',200.00,1,'A bleaching cream to lighten melasma and promote an even complexion.'),(90,'Melasma Sunblock','SKIN CARE PRODUCTS',150.00,1,'A sunblock formulated to protect skin with melasma from UV damage.'),(91,'Niacinamide Aloe Vera Cleansing Soap','SKIN CARE PRODUCTS',200.00,1,'A cleansing soap with niacinamide and aloe vera to brighten and soothe skin.'),(92,'Niacinamide Sunblock','SKIN CARE PRODUCTS',300.00,1,'A niacinamide-infused sunblock to protect and brighten skin.'),(93,'Niacinamide Clarifying Toner','SKIN CARE PRODUCTS',600.00,1,'A clarifying toner with niacinamide to reduce redness and refine pores.'),(94,'Niacinamide Cream','SKIN CARE PRODUCTS',300.00,1,'A niacinamide cream to hydrate and improve skin clarity and texture.'),(95,'Breakout Acne Facial Wash','SKIN CARE PRODUCTS',300.00,1,'A facial wash from the Breakout Set to cleanse and treat acne-prone skin.'),(96,'Breakout Sun Protect Gel','SKIN CARE PRODUCTS',300.00,1,'A sun protection gel from the Breakout Set for acne-prone skin.'),(97,'Breakout Brightening Serum','SKIN CARE PRODUCTS',900.00,1,'A brightening serum from the Breakout Set to reduce acne marks and enhance skin clarity.'),(98,'Breakout Acne Cream','SKIN CARE PRODUCTS',300.00,1,'An acne cream from the Breakout Set to treat and prevent breakouts.'),(99,'Acne Quick Dry Solution','SKIN CARE PRODUCTS',700.00,1,'A fast-acting solution to dry out and treat active acne spots.'),(100,'Acne Tea Tree Liquid Soap','SKIN CARE PRODUCTS',200.00,1,'A tea tree-infused liquid soap to cleanse and soothe acne-prone skin.'),(101,'Acne Cream','SKIN CARE PRODUCTS',300.00,1,'A targeted cream to reduce acne and promote clearer skin.'),(102,'Korean Drip - Single','GLUTATHIONE',1488.00,1,'A single session of Korean-style glutathione IV drip for skin brightening and detoxification.'),(103,'Ultimate Drip - Single','GLUTATHIONE',2488.00,1,'A single session of premium glutathione IV drip for enhanced skin whitening and overall wellness.'),(104,'Collagen Push - 10+2','GLUTATHIONE',6888.00,1,'A 12-session (10+2 free) collagen push treatment to boost skin elasticity and hydration.'),(105,'Collagen Push - Single','GLUTATHIONE',688.00,1,'A single collagen push injection to enhance skin firmness and hydration.'),(106,'Gluta Push - Single','GLUTATHIONE',800.00,1,'A single glutathione push injection for skin brightening and antioxidant benefits.'),(107,'Gluta Push - 5+1 Full Payment','GLUTATHIONE',3888.00,1,'A 6-session (5+1 free) glutathione push package for skin whitening, with full payment upfront.'),(108,'Gluta Push - 1st Session (5+1)','GLUTATHIONE',888.00,1,'The first session of a 6-session (5+1 free) glutathione push package for skin brightening.'),(109,'Gluta Push - 2nd to 5th Sessions (5+1)','GLUTATHIONE',750.00,1,'Sessions 2 to 5 of a 6-session (5+1 free) glutathione push package for skin whitening.'),(110,'Anti-Aging - 10+1 Full Payment','GLUTATHIONE',7888.00,1,'An 11-session (10+1 free) anti-aging glutathione treatment package for skin rejuvenation and wellness.'),(111,'Gluta Push - 2nd to 9th Sessions (10+2)','GLUTATHIONE',1000.00,1,'Sessions 2 to 9 of a 12-session (10+2 free) glutathione push package for enhanced skin brightening.');
/*!40000 ALTER TABLE `services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `suppliers` (
  `supplier_id` int NOT NULL AUTO_INCREMENT,
  `supplier_name` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `accepts_returns` tinyint(1) DEFAULT '0',
  `products_on_the_way` int DEFAULT '0',
  `status` enum('pending','received','cancelled') NOT NULL DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Luzon Dermacare','Neocell - 360','SKIN CARE PRODUCTS','+639123456789','sales@luzondermacare.ph',1,100,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(2,'Visayas Beauty Supply','Nail Polish','NAIL CARE','+639234567890','info@visayasbeautysupply.ph',1,80,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(3,'Mindanao Lash Co.','Synthetic Lashes','BROWS & LASHES','+639345678901','contact@mindanaolashco.ph',1,60,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(4,'Metro Manila Skincare','Facial Cleanser','FACE & BODY','+639456789012','sales@metromanilaskincare.ph',1,70,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(5,'Pinoy Wax Solutions','Waxing Strips','WAXING','+639567890123','orders@pinoywaxsolutions.ph',1,90,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(6,'Cebu Makeup Supplies','Permanent Makeup Pigments','PERMANENT MAKEUP','+639678901234','info@cebumakeupsupplies.ph',1,50,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00'),(7,'Davao Wellness Corp.','Glutathione IV Solution','GLUTATHIONE','+639789012345','supply@davaowellness.ph',1,60,'pending','2025-06-26 22:26:00','2025-06-26 22:26:00');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` varchar(50) NOT NULL,
  `or_number` varchar(50) NOT NULL,
  `service_id` int NOT NULL,
  `customer_name` varchar(100) NOT NULL,
  `customer_phone` varchar(20) NOT NULL,
  `customer_gender` varchar(20) DEFAULT NULL,
  `customer_city` varchar(100) DEFAULT NULL,
  `payment_method` varchar(50) NOT NULL,
  `discount_percentage` decimal(5,2) DEFAULT '0.00',
  `discount_amount` decimal(10,2) DEFAULT '0.00',
  `base_amount` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `coupon_code` varchar(50) DEFAULT NULL,
  `notes` text,
  `transaction_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  UNIQUE KEY `or_number` (`or_number`),
  KEY `service_id` (`service_id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`service_id`) REFERENCES `services` (`service_id`),
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES ('TXN-20250627-92667','OR-20250627-9825',2,'Jhin Arol De Chavez','0923132313','Male','Marikina City','Cash',30.00,1536.00,5120.00,3584.00,'VIP30','2nd session - 6/30/2025','2025-06-27 06:30:56',1);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('admin','staff') NOT NULL,
  `login_time` datetime DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `logout_time` datetime DEFAULT NULL,
  `total_session_time` int DEFAULT '0',
  `reason_for_creation` text,
  `created_by` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_created_by` (`created_by`),
  CONSTRAINT `fk_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin123','Jhon Arol De Chavez','admin','2025-06-27 06:32:42','2025-06-26 21:54:56','2025-06-26 22:33:06','2025-06-27 06:33:06',495,'Testing',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-27  6:33:32
