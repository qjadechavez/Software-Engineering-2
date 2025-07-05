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
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,53,99,'Used in Service','2025-06-26 22:30:56'),(2,54,99,'Used in Service','2025-06-26 22:30:56'),(3,55,49,'Used in Service','2025-06-26 22:30:56'),(4,5,19,'Updated','2025-06-29 21:47:55'),(5,53,98,'Used in Service','2025-06-29 22:07:12'),(6,54,97,'Used in Service','2025-06-29 22:16:17'),(7,54,96,'Used in Service','2025-06-29 22:24:03'),(8,54,96,'Used in Service','2025-06-29 22:24:03'),(9,54,95,'Used in Service','2025-06-29 22:24:03'),(10,53,96,'Used in Service','2025-06-29 22:30:30'),(11,54,93,'Used in Service','2025-06-29 22:36:04'),(12,54,91,'Used in Service','2025-06-29 22:37:40'),(13,54,90,'Used in Service','2025-06-29 22:52:13'),(14,53,95,'Used in Service','2025-06-29 22:58:33'),(15,54,89,'Used in Service','2025-06-29 23:00:56'),(16,53,94,'Used in Service','2025-06-29 23:32:29'),(17,53,92,'Used in Service','2025-06-29 23:39:16'),(18,53,90,'Used in Service','2025-06-29 23:42:58'),(19,54,87,'Used in Service','2025-06-29 23:51:19'),(20,53,88,'Used in Service','2025-06-29 23:53:35'),(21,53,86,'Used in Service','2025-06-30 00:01:37'),(22,53,84,'Used in Service','2025-06-30 00:08:00'),(23,53,83,'Used in Service','2025-06-30 03:20:45'),(24,53,82,'Used in Service','2025-06-30 03:28:42'),(25,52,19,'Updated','2025-06-30 03:32:30'),(26,52,14,'Used in Service','2025-06-30 06:21:10'),(27,52,9,'Used in Service','2025-06-30 06:34:58'),(28,54,85,'Used in Service','2025-06-30 06:37:45'),(29,27,87,'Used in Service','2025-06-30 06:41:38'),(30,27,74,'Used in Service','2025-06-30 06:44:09'),(31,27,61,'Used in Service','2025-06-30 06:45:25'),(32,27,48,'Used in Service','2025-06-30 06:47:18'),(33,27,35,'Used in Service','2025-06-30 06:48:59'),(34,52,4,'Used in Service','2025-06-30 06:50:48'),(35,52,20,'Updated','2025-06-30 06:51:04'),(36,52,15,'Used in Service','2025-06-30 06:53:10'),(37,66,90,'New','2025-06-30 07:02:20'),(38,53,81,'Used in Service','2025-06-30 07:07:27'),(39,54,84,'Used in Service','2025-06-30 07:07:27'),(40,54,83,'Used in Service','2025-07-01 08:31:13'),(41,54,83,'Used in Service','2025-07-01 08:31:13'),(42,56,79,'Used in Service','2025-07-01 08:31:13'),(43,57,159,'Used in Service','2025-07-01 08:31:13'),(44,52,14,'Used in Service','2025-07-01 13:37:31'),(45,50,49,'Used in Service','2025-07-01 13:37:31'),(46,5,18,'Used in Service','2025-07-01 13:37:31'),(47,52,9,'Used in Service','2025-07-01 13:38:50'),(48,56,78,'Used in Service','2025-07-01 13:40:19'),(49,57,158,'Used in Service','2025-07-01 13:40:19'),(50,27,22,'Used in Service','2025-07-01 13:43:03'),(51,50,48,'Used in Service','2025-07-01 13:43:03'),(52,5,17,'Used in Service','2025-07-01 13:43:03'),(53,66,89,'Used in Service','2025-07-01 13:43:03'),(54,27,9,'Used in Service','2025-07-01 13:44:38'),(55,50,47,'Used in Service','2025-07-01 13:44:38'),(56,5,16,'Used in Service','2025-07-01 13:44:38'),(57,66,88,'Used in Service','2025-07-01 13:44:38'),(58,27,0,'Used in Service','2025-07-01 13:45:16'),(59,50,46,'Used in Service','2025-07-01 13:45:16'),(60,5,15,'Used in Service','2025-07-01 13:45:16'),(61,66,87,'Used in Service','2025-07-01 13:45:16'),(62,56,77,'Used in Service','2025-07-02 04:33:14'),(63,57,157,'Used in Service','2025-07-02 04:33:14'),(64,54,0,'Updated','2025-07-02 22:38:49');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_batches`
--

DROP TABLE IF EXISTS `inventory_batches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_batches` (
  `batch_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `original_quantity` int NOT NULL DEFAULT '0',
  `supplier_name` varchar(255) DEFAULT NULL,
  `received_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('active','depleted','expired') DEFAULT 'active',
  PRIMARY KEY (`batch_id`),
  KEY `idx_product_expiry` (`product_id`,`expiry_date`),
  KEY `idx_expiry_date` (`expiry_date`),
  KEY `idx_product_name` (`product_name`),
  CONSTRAINT `inventory_batches_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_batches`
--

LOCK TABLES `inventory_batches` WRITE;
/*!40000 ALTER TABLE `inventory_batches` DISABLE KEYS */;
/*!40000 ALTER TABLE `inventory_batches` ENABLE KEYS */;
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
  `batch_id` int DEFAULT NULL,
  PRIMARY KEY (`inventory_id`),
  UNIQUE KEY `unique_product` (`product_id`),
  CONSTRAINT `inventory_status_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2488 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_status`
--

LOCK TABLES `inventory_status` WRITE;
/*!40000 ALTER TABLE `inventory_status` DISABLE KEYS */;
INSERT INTO `inventory_status` VALUES (1,1,'Neocell - 360',150,'In Stock','Luzon Dermacare','2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(2,2,'Hydrocort',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(3,3,'Underarm Set',30,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(4,4,'Clear Set Whitening Set',40,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(5,5,'Acne Set',15,'Low Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(6,6,'Breakout Set',35,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(7,7,'Warts Set',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(8,8,'Melasma Set',40,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(9,9,'Niacinamide Set',30,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(10,10,'Rejuv Set',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(11,11,'Gluta Lotion Tomato',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(12,12,'Glutathione Lotion',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(13,13,'Bleaching Lotion',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(14,14,'Whipped Scrub',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(15,15,'Gluta Liquid Soap',70,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(16,16,'Instawhite Lotion',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(17,17,'Collagen Serum',40,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(18,18,'Vitamin C & E Serum',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(19,19,'Niacinamide Serum',40,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(20,20,'Underarm Toner',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(21,21,'Underarm Liquid Gluta Soap',70,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(22,22,'Underarm Whitening Cream',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(23,23,'Underarm Deo Whitening Spray',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(24,24,'BAR SOAP - NIACINAMIDE',80,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(25,25,'BAR SOAP - COLLAGEN',80,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(26,26,'BAR SOAP - PAPAYA',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(27,27,'BAR SOAP - KOJIC',0,'Out of Stock',NULL,'2025-07-01 21:45:16','2025-06-26 22:19:52',NULL),(28,28,'BAR SOAP - GLUTA KOJIC',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(29,29,'BAR SOAP - OATMEAL SOAP',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(30,30,'Moisturizing Soap',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(31,31,'Clear Set Clarifying Toner No1',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(32,32,'Clear Set Whitening Toner No2',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(33,33,'Clear Set Night Cream 4',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(34,34,'Clear Set Night Cream 5',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(35,35,'Clear Set Sunblock',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(36,36,'Oatmeal Soap',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(37,37,'Melasma Toner',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(38,38,'Melasma Medicated Toner',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(39,39,'Melasma Cream',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(40,40,'Melasma Bleaching Cream',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(41,41,'Melasma Sunblock',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(42,42,'Niacinamide Aloe Vera Cleansing Soap',80,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(43,43,'Niacinamide Sunblock',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(44,44,'Niacinamide Clarifying Toner',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(45,45,'Niacinamide Cream',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(46,46,'Breakout Acne Facial Wash',70,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(47,47,'Breakout Sun Protect Gel',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(48,48,'Breakout Brightening Serum',40,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(49,49,'Breakout Acne Cream',60,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(50,50,'Acne Quick Dry Solution',46,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(51,51,'Acne Tea Tree Liquid Soap',70,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(52,52,'Acne Cream',500,'Received','Testing','2025-07-03 10:50:55','2025-06-26 22:19:52',NULL),(53,53,'Nail Polish',80,'Received','Visayas Beauty Supply','2025-07-03 08:32:42','2025-06-26 22:19:52',NULL),(54,54,'UV Gel Polish',0,'Out of Stock',NULL,'2025-07-03 06:38:49','2025-06-26 22:19:52',NULL),(55,55,'Nail Extension Material',49,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(56,56,'Eyelash Extension Adhesive',77,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(57,57,'Synthetic Lashes',157,'In Stock','Mindanao Lash Co.','2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(58,58,'Facial Cleanser',120,'In Stock','Metro Manila Skincare','2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(59,59,'Chemical Peel Solution',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(60,60,'Waxing Strips',90,'Received','Pinoy Wax Solutions','2025-07-03 08:02:24','2025-06-26 22:19:52',NULL),(61,61,'Waxing Solution',100,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(62,62,'Permanent Makeup Pigments',100,'In Stock','Cebu Makeup Supplies','2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(63,63,'BB Glow Pigments',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(64,64,'Glutathione IV Solution',110,'In Stock','Davao Wellness Corp.','2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(65,65,'Collagen IV Solution',50,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-26 22:19:52',NULL),(106,66,'Lotion',87,'In Stock',NULL,'2025-07-03 03:56:31','2025-06-30 07:02:20',NULL);
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
  `batch_id` int DEFAULT NULL,
  PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_transactions`
--

LOCK TABLES `inventory_transactions` WRITE;
/*!40000 ALTER TABLE `inventory_transactions` DISABLE KEYS */;
INSERT INTO `inventory_transactions` VALUES (1,'Facial Cleanser','Stock In',70,'Received from supplier: Metro Manila Skincare','2025-06-27 08:32:37','2025-06-27 00:32:37',NULL),(2,'Glutathione IV Solution','Stock In',60,'Received from supplier: Davao Wellness Corp.','2025-06-30 14:01:05','2025-06-30 06:01:05',NULL),(3,'Synthetic Lashes','Stock In',60,'Received from supplier: Mindanao Lash Co.','2025-06-30 15:13:32','2025-06-30 07:13:32',NULL),(4,'Permanent Makeup Pigments','Stock In',50,'Received from supplier: Cebu Makeup Supplies','2025-06-30 15:27:47','2025-06-30 07:27:47',NULL),(5,'Neocell - 360','Stock In',100,'Received from supplier: Luzon Dermacare','2025-07-02 22:51:05','2025-07-02 14:51:05',NULL),(6,'Waxing Strips','Stock In',90,'Received from supplier: Pinoy Wax Solutions','2025-07-03 08:02:24','2025-07-03 00:02:24',NULL),(7,'Nail Polish','Stock In',80,'Received from supplier: Visayas Beauty Supply (Expires: 2024-01-03)','2025-07-03 08:32:42','2025-07-03 00:32:42',NULL),(8,'Acne Cream','Stock In',500,'Received from supplier: Testing','2025-07-03 10:50:55','2025-07-03 02:50:55',NULL);
/*!40000 ALTER TABLE `inventory_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product_batches`
--

DROP TABLE IF EXISTS `product_batches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product_batches` (
  `batch_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `category` varchar(100) DEFAULT NULL,
  `quantity` int NOT NULL DEFAULT '0',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `expiry_date` date DEFAULT NULL,
  `batch_code` varchar(100) DEFAULT NULL,
  `supplier_name` varchar(255) DEFAULT NULL,
  `received_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`batch_id`),
  KEY `idx_product_expiry` (`product_id`,`expiry_date`),
  KEY `idx_expiry_date` (`expiry_date`),
  CONSTRAINT `product_batches_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product_batches`
--

LOCK TABLES `product_batches` WRITE;
/*!40000 ALTER TABLE `product_batches` DISABLE KEYS */;
/*!40000 ALTER TABLE `product_batches` ENABLE KEYS */;
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
  `abc_category` varchar(1) DEFAULT 'C',
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Neocell - 360','A comprehensive skin supplement to promote collagen production and overall skin health.','SKIN CARE PRODUCTS',2500.00,150,20,'2026-06-27','/icons/neocell_360.png',1,'Active','A'),(2,'Hydrocort','A hydrocortisone-based cream to reduce inflammation and soothe irritated skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/hydrocort.png',1,'Active','B'),(3,'Underarm Set','A complete underarm care kit for whitening and smoothening the underarm area.','SKIN CARE PRODUCTS',700.00,30,20,'2026-06-27','/icons/underarm_set.png',1,'Active','A'),(4,'Clear Set Whitening Set','A skincare set designed to brighten and even out skin tone for a radiant complexion.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/clear_set_whitening.png',1,'Active','A'),(5,'Acne Set','A targeted skincare set to treat and prevent acne, including cleansing and treatment products.','SKIN CARE PRODUCTS',1500.00,15,20,'2026-06-27','/icons/acne_set.png',1,'Active','A'),(6,'Breakout Set','A specialized set to address acne breakouts and promote clearer, healthier skin.','SKIN CARE PRODUCTS',1800.00,35,20,'2026-06-27','/icons/breakout_set.png',1,'Active','A'),(7,'Warts Set','A treatment kit designed to target and reduce the appearance of warts.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/warts_set.png',1,'Active','A'),(8,'Melasma Set','A skincare set formulated to reduce melasma and hyperpigmentation for even-toned skin.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/melasma_set.png',1,'Active','A'),(9,'Niacinamide Set','A complete niacinamide-based skincare set to brighten skin and minimize pores.','SKIN CARE PRODUCTS',2500.00,30,20,'2026-06-27','/icons/niacinamide_set.png',1,'Active','A'),(10,'Rejuv Set','A rejuvenating skincare set to hydrate and revitalize the skin for a youthful glow.','SKIN CARE PRODUCTS',600.00,50,20,'2026-06-27','/icons/rejuv_set.png',1,'Active','A'),(11,'Gluta Lotion Tomato','A glutathione and tomato-infused lotion for skin brightening and hydration.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/gluta_lotion_tomato.png',1,'Active','A'),(12,'Glutathione Lotion','A lotion with glutathione to promote skin whitening and a smoother complexion.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/glutathione_lotion.png',1,'Active','A'),(13,'Bleaching Lotion','A skin-lightening lotion to reduce dark spots and even out skin tone.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/bleaching_lotion.png',1,'Active','A'),(14,'Whipped Scrub','A whipped exfoliating scrub to remove dead skin and promote a smooth, radiant complexion.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/whipped_scrub.png',1,'Active','A'),(15,'Gluta Liquid Soap','A liquid soap infused with glutathione for gentle cleansing and skin brightening.','SKIN CARE PRODUCTS',300.00,70,20,'2026-06-27','/icons/gluta_liquid_soap.png',1,'Active','A'),(16,'Instawhite Lotion','A fast-acting whitening lotion to brighten and hydrate the skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/instawhite_lotion.png',1,'Active','A'),(17,'Collagen Serum','A collagen-infused serum to improve skin elasticity and reduce signs of aging.','SKIN CARE PRODUCTS',1000.00,40,20,'2026-06-27','/icons/collagen_serum.png',1,'Active','A'),(18,'Vitamin C & E Serum','A serum with vitamins C and E to brighten skin and protect against environmental damage.','SKIN CARE PRODUCTS',850.00,50,20,'2026-06-27','/icons/vitamin_c_e_serum.png',1,'Active','A'),(19,'Niacinamide Serum','A niacinamide serum to minimize pores, reduce redness, and enhance skin clarity.','SKIN CARE PRODUCTS',1500.00,40,20,'2026-06-27','/icons/niacinamide_serum.png',1,'Active','A'),(20,'Underarm Toner','A toner designed to brighten and smooth the underarm area.','SKIN CARE PRODUCTS',400.00,50,20,'2026-06-27','/icons/underarm_toner.png',1,'Active','A'),(21,'Underarm Liquid Gluta Soap','A liquid soap with glutathione for cleansing and whitening the underarm area.','SKIN CARE PRODUCTS',150.00,70,20,'2026-06-27','/icons/underarm_gluta_soap.png',1,'Active','B'),(22,'Underarm Whitening Cream','A cream formulated to lighten and soften underarm skin.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/underarm_whitening_cream.png',1,'Active','C'),(23,'Underarm Deo Whitening Spray','A deodorizing spray with whitening properties for underarm care.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/underarm_deo_spray.png',1,'Active','C'),(24,'BAR SOAP - NIACINAMIDE','A niacinamide-infused bar soap for cleansing and brightening the skin.','SKIN CARE PRODUCTS',250.00,80,20,'2026-06-27','/icons/bar_soap_niacinamide.png',1,'Active','A'),(25,'BAR SOAP - COLLAGEN','A collagen-enriched bar soap to hydrate and improve skin elasticity.','SKIN CARE PRODUCTS',250.00,80,20,'2026-06-27','/icons/bar_soap_collagen.png',1,'Active','A'),(26,'BAR SOAP - PAPAYA','A papaya-based bar soap for gentle exfoliation and skin brightening.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_papaya.png',1,'Active','B'),(27,'BAR SOAP - KOJIC','A kojic acid bar soap to reduce dark spots and promote even skin tone.','SKIN CARE PRODUCTS',150.00,0,20,'2026-06-27','/icons/bar_soap_kojic.png',0,'Active','C'),(28,'BAR SOAP - GLUTA KOJIC','A bar soap with glutathione and kojic acid for enhanced skin whitening and cleansing.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_gluta_kojic.png',1,'Active','B'),(29,'BAR SOAP - OATMEAL SOAP','An oatmeal bar soap for gentle exfoliation and soothing sensitive skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/bar_soap_oatmeal.png',1,'Active','B'),(30,'Moisturizing Soap','A hydrating soap to cleanse and moisturize the skin, leaving it soft and smooth.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/moisturizing_soap.png',1,'Active','B'),(31,'Clear Set Clarifying Toner No1','A clarifying toner from the Clear Set to cleanse and prepare skin for further treatment.','SKIN CARE PRODUCTS',350.00,50,20,'2026-06-27','/icons/clear_set_toner_no1.png',1,'Active','B'),(32,'Clear Set Whitening Toner No2','A whitening toner from the Clear Set to brighten and even out skin tone.','SKIN CARE PRODUCTS',400.00,50,20,'2026-06-27','/icons/clear_set_toner_no2.png',1,'Active','A'),(33,'Clear Set Night Cream 4','A night cream from the Clear Set to hydrate and repair skin overnight.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_night_cream_4.png',1,'Active','C'),(34,'Clear Set Night Cream 5','An advanced night cream from the Clear Set for intensive skin nourishment.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_night_cream_5.png',1,'Active','C'),(35,'Clear Set Sunblock','A sunblock from the Clear Set to protect skin from UV damage.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/clear_set_sunblock.png',1,'Active','B'),(36,'Oatmeal Soap','An oatmeal-based soap for gentle cleansing and soothing irritated or sensitive skin.','SKIN CARE PRODUCTS',150.00,100,20,'2026-06-27','/icons/oatmeal_soap.png',1,'Active','B'),(37,'Melasma Toner','A toner formulated to reduce melasma and hyperpigmentation for clearer skin.','SKIN CARE PRODUCTS',500.00,50,20,'2026-06-27','/icons/melasma_toner.png',1,'Active','A'),(38,'Melasma Medicated Toner','A medicated toner to target melasma and even out skin tone.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_medicated_toner.png',1,'Active','B'),(39,'Melasma Cream','A cream designed to treat melasma and reduce dark spots.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_cream.png',1,'Active','B'),(40,'Melasma Bleaching Cream','A bleaching cream to lighten melasma and promote an even complexion.','SKIN CARE PRODUCTS',200.00,60,20,'2026-06-27','/icons/melasma_bleaching_cream.png',1,'Active','B'),(41,'Melasma Sunblock','A sunblock formulated to protect skin with melasma from UV damage.','SKIN CARE PRODUCTS',150.00,60,20,'2026-06-27','/icons/melasma_sunblock.png',1,'Active','C'),(42,'Niacinamide Aloe Vera Cleansing Soap','A cleansing soap with niacinamide and aloe vera to brighten and soothe skin.','SKIN CARE PRODUCTS',200.00,80,20,'2026-06-27','/icons/niacinamide_aloe_soap.png',1,'Active','B'),(43,'Niacinamide Sunblock','A niacinamide-infused sunblock to protect and brighten skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/niacinamide_sunblock.png',1,'Active','B'),(44,'Niacinamide Clarifying Toner','A clarifying toner with niacinamide to reduce redness and refine pores.','SKIN CARE PRODUCTS',600.00,50,20,'2026-06-27','/icons/niacinamide_clarifying_toner.png',1,'Active','A'),(45,'Niacinamide Cream','A niacinamide cream to hydrate and improve skin clarity and texture.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/niacinamide_cream.png',1,'Active','B'),(46,'Breakout Acne Facial Wash','A facial wash from the Breakout Set to cleanse and treat acne-prone skin.','SKIN CARE PRODUCTS',300.00,70,20,'2026-06-27','/icons/breakout_acne_wash.png',1,'Active','A'),(47,'Breakout Sun Protect Gel','A sun protection gel from the Breakout Set for acne-prone skin.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/breakout_sun_protect_gel.png',1,'Active','A'),(48,'Breakout Brightening Serum','A brightening serum from the Breakout Set to reduce acne marks and enhance skin clarity.','SKIN CARE PRODUCTS',900.00,40,20,'2026-06-27','/icons/breakout_brightening_serum.png',1,'Active','A'),(49,'Breakout Acne Cream','An acne cream from the Breakout Set to treat and prevent breakouts.','SKIN CARE PRODUCTS',300.00,60,20,'2026-06-27','/icons/breakout_acne_cream.png',1,'Active','A'),(50,'Acne Quick Dry Solution','A fast-acting solution to dry out and treat active acne spots.','SKIN CARE PRODUCTS',700.00,46,20,'2026-06-27','/icons/acne_quick_dry_solution.png',1,'Active','A'),(51,'Acne Tea Tree Liquid Soap','A tea tree-infused liquid soap to cleanse and soothe acne-prone skin.','SKIN CARE PRODUCTS',200.00,70,20,'2026-06-27','/icons/acne_tea_tree_soap.png',1,'Active','B'),(52,'Acne Cream','A targeted cream to reduce acne and promote clearer skin.','SKIN CARE PRODUCTS',300.00,609,20,'2026-06-27','/icons/acne_cream.png',1,'Active','C'),(53,'Nail Polish','Standard nail polish used in manicure and pedicure services.','NAIL CARE',10.00,161,15,'2024-01-03','/icons/nail_polish.png',1,'Active','C'),(54,'UV Gel Polish','UV-curable gel polish for long-lasting manicures and pedicures.','NAIL CARE',20.00,0,15,'2026-06-27','/icons/uv_gel_polish.png',1,'Active','C'),(55,'Nail Extension Material','Materials for applying nail extensions, including acrylic or gel.','NAIL CARE',50.00,49,15,'2026-06-27','/icons/nail_extension_material.png',1,'Active','C'),(56,'Eyelash Extension Adhesive','Adhesive used for applying eyelash extensions.','BROWS & LASHES',30.00,77,15,'2026-06-27','/icons/eyelash_adhesive.png',1,'Active','C'),(57,'Synthetic Lashes','Synthetic lashes for classic and volume eyelash extension services.','BROWS & LASHES',25.00,157,15,'2026-06-27','/icons/synthetic_lashes.png',1,'Active','C'),(58,'Facial Cleanser','Cleanser used in facial treatments for cleansing and preparation.','FACE & BODY',15.00,120,15,'2026-06-27','/icons/facial_cleanser.png',1,'Active','C'),(59,'Chemical Peel Solution','Solution used for chemical peel facials to exfoliate and renew skin.','FACE & BODY',40.00,50,15,'2026-06-27','/icons/chemical_peel_solution.png',1,'Active','C'),(60,'Waxing Strips','Strips used for waxing services to remove hair.','WAXING',10.00,190,15,'2026-06-27','/icons/waxing_strips.png',1,'Active','C'),(61,'Waxing Solution','Wax solution used for hair removal in waxing services.','WAXING',15.00,100,15,'2026-06-27','/icons/waxing_solution.png',1,'Active','C'),(62,'Permanent Makeup Pigments','Pigments used for microshading, microblading, and eyeliner services.','PERMANENT MAKEUP',30.00,100,15,'2026-06-27','/icons/permanent_makeup_pigments.png',1,'Active','C'),(63,'BB Glow Pigments','Pigments used for Korean BB Glow treatments for semi-permanent makeup.','PERMANENT MAKEUP',35.00,50,15,'2026-06-27','/icons/bb_glow_pigments.png',1,'Active','C'),(64,'Glutathione IV Solution','IV solution used for glutathione drip and push treatments.','GLUTATHIONE',50.00,110,15,'2026-03-27','/icons/glutathione_iv_solution.png',1,'Active','C'),(65,'Collagen IV Solution','IV solution used for collagen push treatments.','GLUTATHIONE',50.00,50,15,'2026-03-27','/icons/collagen_iv_solution.png',1,'Active','C'),(66,'Lotion','','Skinscre',90.00,87,10,'2026-06-30',NULL,1,'In Stock','C');
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
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_products`
--

LOCK TABLES `service_products` WRITE;
/*!40000 ALTER TABLE `service_products` DISABLE KEYS */;
INSERT INTO `service_products` VALUES (1,1,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(2,2,53,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(3,3,53,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(4,4,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(5,5,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(7,7,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(8,8,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(16,16,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(17,17,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(18,18,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(19,19,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(20,20,54,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(21,21,54,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(22,22,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(23,23,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(24,24,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(25,25,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(26,26,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(27,27,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(28,28,55,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(29,31,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(30,31,57,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(31,32,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(32,32,57,2,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(33,33,56,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(34,33,57,3,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(35,34,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(36,35,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(37,36,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(38,37,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(39,37,46,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(40,38,58,1,'2025-06-26 22:20:00','2025-06-26 22:20:00'),(41,30,52,5,'2025-06-30 06:16:40','2025-06-30 06:16:40'),(43,12,27,13,'2025-06-30 07:03:23','2025-06-30 07:03:23'),(44,12,50,1,'2025-06-30 07:03:23','2025-06-30 07:03:23'),(45,12,5,1,'2025-06-30 07:03:23','2025-06-30 07:03:23'),(46,12,66,1,'2025-06-30 07:03:23','2025-06-30 07:03:23'),(50,6,56,1,'2025-07-01 08:06:28','2025-07-01 08:06:28'),(51,6,57,1,'2025-07-01 08:06:28','2025-07-01 08:06:28'),(52,10,52,1,'2025-07-01 08:07:18','2025-07-01 08:07:18'),(53,10,50,1,'2025-07-01 08:07:18','2025-07-01 08:07:18'),(54,10,5,1,'2025-07-01 08:07:18','2025-07-01 08:07:18'),(55,13,52,1,'2025-07-01 08:08:12','2025-07-01 08:08:12'),(56,13,5,1,'2025-07-01 08:08:12','2025-07-01 08:08:12'),(57,14,58,1,'2025-07-01 08:08:36','2025-07-01 08:08:36'),(58,14,46,1,'2025-07-01 08:08:36','2025-07-01 08:08:36'),(59,15,58,1,'2025-07-01 08:09:00','2025-07-01 08:09:00'),(60,15,46,1,'2025-07-01 08:09:00','2025-07-01 08:09:00'),(61,11,58,1,'2025-07-01 08:10:18','2025-07-01 08:10:18'),(62,11,46,1,'2025-07-01 08:10:18','2025-07-01 08:10:18'),(63,11,51,1,'2025-07-01 08:10:18','2025-07-01 08:10:18'),(64,9,27,1,'2025-07-01 08:11:02','2025-07-01 08:11:02'),(65,9,24,1,'2025-07-01 08:11:02','2025-07-01 08:11:02'),(66,9,29,1,'2025-07-01 08:11:02','2025-07-01 08:11:02'),(67,9,52,1,'2025-07-01 08:11:02','2025-07-01 08:11:02');
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
) ENGINE=InnoDB AUTO_INCREMENT=113 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `expiry_date` date DEFAULT NULL,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Luzon Dermacare','Neocell - 360','SKIN CARE PRODUCTS','+639123456789','sales@luzondermacare.ph',1,0,'received','2025-06-26 22:26:00','2025-07-02 14:51:05',NULL),(2,'Visayas Beauty Supply','Nail Polish','NAIL CARE','+639234567890','info@visayasbeautysupply.ph',1,0,'received','2025-06-26 22:26:00','2025-07-03 00:32:42','2024-01-03'),(3,'Mindanao Lash Co.','Synthetic Lashes','BROWS & LASHES','+639345678901','contact@mindanaolashco.ph',1,0,'received','2025-06-26 22:26:00','2025-06-30 07:13:32',NULL),(4,'Metro Manila Skincare','Facial Cleanser','FACE & BODY','+639456789012','sales@metromanilaskincare.ph',1,0,'received','2025-06-26 22:26:00','2025-06-27 00:32:37',NULL),(5,'Pinoy Wax Solutions','Waxing Strips','WAXING','+639567890123','orders@pinoywaxsolutions.ph',1,0,'received','2025-06-26 22:26:00','2025-07-03 00:02:24',NULL),(6,'Cebu Makeup Supplies','Permanent Makeup Pigments','PERMANENT MAKEUP','+639678901234','info@cebumakeupsupplies.ph',1,0,'received','2025-06-26 22:26:00','2025-06-30 07:27:47',NULL),(7,'Davao Wellness Corp.','Glutathione IV Solution','GLUTATHIONE','+639789012345','supply@davaowellness.ph',1,0,'received','2025-06-26 22:26:00','2025-06-30 06:01:05',NULL),(8,'Tesing','Acne Cream','Skin Care Products','09213213','awdawd@gmail.com',1,100,'received','2025-07-03 00:52:00','2025-07-03 02:14:19','2024-07-03'),(9,'Testing','Acne Cream','SKIN CARE PRODUCTS','21e21e','wdwe1e',1,0,'received','2025-07-03 02:50:49','2025-07-03 02:50:55',NULL);
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
INSERT INTO `transactions` VALUES ('TXN-20250627-92667','OR-20250627-9825',2,'Jhin Arol De Chavez','0923132313','Male','Marikina City','Cash',30.00,1536.00,5120.00,3584.00,'VIP30','2nd session - 6/30/2025','2025-06-27 06:30:56',1),('TXN-20250630-12959','OR-20250630-9884',12,'wadw','aw','','dawd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 08:01:37',1),('TXN-20250630-14062','OR-20250630-6618',12,'wadaw','wad','','awd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 08:08:00',1),('TXN-20250630-16150','OR-20250630-7769',6,'wadw','wad','','ad','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 06:37:40',1),('TXN-20250630-22282','OR-20250630-9839',10,'wad','awd','','awd','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 06:07:12',1),('TXN-20250630-27135','OR-20250630-1115',30,'jhon','jhon','','jhon','Cash',0.00,0.00,7000.00,7000.00,'','','2025-06-30 14:50:48',1),('TXN-20250630-31985','OR-20250630-1149',7,'awdwa','awdaw','','awdawdaw','Cash',0.00,0.00,800.00,800.00,'','','2025-06-30 07:00:56',1),('TXN-20250630-35357','OR-20250630-6436',14,'mont','0912345678','Male','montalban','Cash',10.00,1838.80,18388.00,16549.20,'WELCOME10','','2025-06-30 15:07:27',4),('TXN-20250630-40675','OR-20250630-1911',4,'Test','09155288980','Male','Marikina City','Cash',0.00,0.00,3300.00,3300.00,'','','2025-06-30 06:24:03',1),('TXN-20250630-41732','OR-20250630-4094',12,'test','test','','test','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 14:47:18',1),('TXN-20250630-42603','OR-20250630-9816',6,'adwawd','wadawdwa','','awda','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 14:37:45',1),('TXN-20250630-47521','OR-20250630-8669',12,'AWDAW','AWDAW','','AWDAWD','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 07:53:35',1),('TXN-20250630-51864','OR-20250630-2133',12,'jhon','wa daw','Male','dawd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 06:30:30',1),('TXN-20250630-52547','OR-20250630-8701',12,'wad','awd','','awd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 07:42:58',1),('TXN-20250630-54060','OR-20250630-3224',12,'awdaw','awdaw','','awdawd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 14:41:38',1),('TXN-20250630-59936','OR-20250630-6557',13,'wdawaw','wad','','awdaw','Cash',0.00,0.00,1800.00,1800.00,'','','2025-06-30 11:28:42',1),('TXN-20250630-69644','OR-20250630-8617',11,'awd','aw','','awd','Cash',0.00,0.00,1800.00,1800.00,'','','2025-06-30 06:58:33',1),('TXN-20250630-72666','OR-20250630-1853',12,'jhon','wdaw','','wdawda','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 14:48:59',1),('TXN-20250630-77974','OR-20250630-5781',30,'test','09162312','','adwadwq','Cash',0.00,0.00,7000.00,7000.00,'','','2025-06-30 14:53:10',1),('TXN-20250630-78122','OR-20250630-2842',8,'dwadaw','dawda','Male','adwawdwa','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 06:52:13',1),('TXN-20250630-79664','OR-20250630-6295',6,'testing','tesing','Male','marikina city','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 06:16:17',1),('TXN-20250630-80195','OR-20250630-3101',30,'awdwda','awd','','awdaw','Cash',0.00,0.00,7000.00,7000.00,'','','2025-06-30 14:34:58',1),('TXN-20250630-81328','OR-20250630-5752',13,'testing','dwdwad','','adw','Cash',0.00,0.00,1800.00,1800.00,'','','2025-06-30 11:20:45',1),('TXN-20250630-82006','OR-20250630-4795',13,'awwwwwwwwwwwwwwwwwwwwwwwwwww','waaaaaaaaaaaaaaaa','','wwwwwwwwwwwwwwww','Cash',0.00,0.00,1800.00,1800.00,'','','2025-06-30 07:32:29',1),('TXN-20250630-82809','OR-20250630-7953',6,'adwadwdawdaw','awdawda','Male','awdawd','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 06:36:04',1),('TXN-20250630-83862','OR-20250630-8377',12,'awdwada','awda','','wdawd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 07:39:16',1),('TXN-20250630-91027','OR-20250630-7749',30,'wadawd','wadawawadwad','Male','awdwadwa','Cash',0.00,0.00,7000.00,7000.00,'','','2025-06-30 14:21:10',1),('TXN-20250630-91449','OR-20250630-5631',6,'TETING','TETING','','TETING','Cash',0.00,0.00,1500.00,1500.00,'','','2025-06-30 07:51:19',1),('TXN-20250630-96704','OR-20250630-4718',12,'awdadwa','awdwada','','ww','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 14:45:25',1),('TXN-20250630-97360','OR-20250630-3834',12,'awdw','awdad','','awdaw','Cash',0.00,0.00,2500.00,2500.00,'','','2025-06-30 14:44:09',1),('TXN-20250630-97947','OR-20250630-9912',110,'Kyrie','09155288980','Male','Marikna City','Cash',0.00,0.00,7888.00,7888.00,'','','2025-06-30 06:51:06',1),('TXN-20250701-34447','OR-20250701-9864',12,'wad','awd','Male','awd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-07-01 21:45:16',1),('TXN-20250701-46054','OR-20250701-6213',31,'awd','awd','Male','awdawd','Cash',0.00,0.00,5000.00,5000.00,'','','2025-07-01 21:40:19',1),('TXN-20250701-48314','OR-20250701-6442',10,'jhon','0921321','Male','wdawda','Cash',0.00,0.00,1500.00,1500.00,'','','2025-07-01 21:37:31',1),('TXN-20250701-67148','OR-20250701-3279',12,'awd','aw','Male','awdwad','Cash',0.00,0.00,2500.00,2500.00,'','','2025-07-01 21:43:03',1),('TXN-20250701-67343','OR-20250701-4567',30,'wadw','awda','Male','awdwad','Cash',0.00,0.00,7000.00,7000.00,'','','2025-07-01 21:38:50',1),('TXN-20250701-83767','OR-20250701-4783',4,'test','0912345678','Male','marikina xcity','Cash',10.00,330.00,3300.00,2970.00,'WELCOME10','TEST','2025-07-01 16:31:13',1),('TXN-20250701-84506','OR-20250701-1753',12,'wad','aw','Male','awd','Cash',0.00,0.00,2500.00,2500.00,'','','2025-07-01 21:44:38',1),('TXN-20250702-45010','OR-20250702-8631',6,'awdaw','sawdawd','','sdawdwad','Cash',0.00,0.00,1500.00,1500.00,'','','2025-07-02 12:33:14',1);
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
  `security_question` varchar(255) DEFAULT NULL,
  `security_answer` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  KEY `fk_created_by` (`created_by`),
  CONSTRAINT `fk_created_by` FOREIGN KEY (`created_by`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','admin123','Juan Dela Cruz','admin','2025-07-03 12:42:04','2025-06-26 21:54:56','2025-07-03 04:42:03','2025-07-03 12:12:43',32596,'Default system administrator account',NULL,'What is your favorite color?','blue'),(2,'Maria','ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae','Maria','staff','2025-06-30 11:45:31','2025-06-29 21:33:29','2025-06-30 03:45:33','2025-06-30 11:45:33',17,'new account',1,NULL,NULL),(3,'Lebron','lebron123','Lebron James','admin','2025-06-30 11:39:40','2025-06-29 21:56:50','2025-06-30 03:41:08',NULL,0,'new admin	account',NULL,NULL,NULL),(4,'Mont','4dd3b5aa8aea438b027492ba0cab9fdebdd50365b72a634cab1978b71982945d','Mont Cabe','staff','2025-06-30 15:01:37','2025-06-30 07:01:25','2025-06-30 07:28:39','2025-06-30 15:28:39',1622,'newly hired staff',1,NULL,NULL),(5,'Jhon','9376cc7a21a33b81c3f433951fb6009beb4e85b7a711f71c0c4775d35a461033','JhonArol','staff','2025-07-03 11:18:19','2025-07-03 03:18:04','2025-07-03 03:18:19',NULL,0,'dwa',1,NULL,NULL),(9,'testing','b822f1cd2dcfc685b47e83e3980289fd5d8e3ff3a82def24d7d1d68bb272eb32','Testing','staff',NULL,'2025-07-03 04:09:01','2025-07-03 04:09:01',NULL,0,'wadwa',1,'What is your favorite color?','blue'),(10,'admin123','240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9','System Administrator','admin','2025-07-03 12:13:54','2025-07-03 04:10:00','2025-07-03 04:13:53','2025-07-03 12:13:01',10,'Default system administrator account',NULL,'What is your favorite color?','blue'),(11,'test','ecd71870d1963316a97e3ac3408c9835ad8cf0f3c1bc703527c30265534f75ae','test','staff',NULL,'2025-07-03 04:10:50','2025-07-03 04:10:50',NULL,0,'awd',10,'What is your favorite color?','blue');
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

-- Dump completed on 2025-07-03 14:03:56
