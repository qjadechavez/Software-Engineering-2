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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,15,50,'Updated','2025-06-26 13:04:55'),(2,16,50,'Updated','2025-06-26 13:06:11'),(3,16,50,'Updated','2025-06-26 13:06:31'),(4,16,50,'Updated','2025-06-26 13:08:31'),(5,15,50,'Updated','2025-06-26 13:08:43'),(6,18,25,'Updated','2025-06-26 13:10:28'),(7,17,20,'Updated','2025-06-26 13:10:49'),(8,16,49,'Used in Service','2025-06-26 13:31:01'),(9,15,49,'Used in Service','2025-06-26 13:31:01'),(10,18,19,'Used in Service','2025-06-26 15:25:44'),(11,17,14,'Used in Service','2025-06-26 15:25:44'),(12,18,18,'Used in Service','2025-06-26 15:38:28'),(13,17,13,'Used in Service','2025-06-26 15:38:28'),(14,16,48,'Used in Service','2025-06-26 15:51:54'),(15,15,48,'Used in Service','2025-06-26 15:51:54');
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
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_status`
--

LOCK TABLES `inventory_status` WRITE;
/*!40000 ALTER TABLE `inventory_status` DISABLE KEYS */;
INSERT INTO `inventory_status` VALUES (1,15,'Hair Shampoo',48,'In Stock','Beauty Essentials Co.','2025-06-26 23:51:54','2025-06-26 13:04:17'),(4,16,'Hair Dye',48,'In Stock','ColorTrend Ltd.','2025-06-26 23:51:54','2025-06-26 13:05:37'),(10,17,'Facial Cleanser',13,'In Stock','SalonBasics','2025-06-26 23:38:28','2025-06-26 13:09:57'),(12,18,'Face Mask',18,'In Stock','SkinVibe Dist.','2025-06-26 23:38:28','2025-06-26 13:10:01'),(34,19,'Eyebrow Gel',20,'Received','BeautyTrend Co.','2025-06-27 00:18:22','2025-06-26 16:18:22');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_transactions`
--

LOCK TABLES `inventory_transactions` WRITE;
/*!40000 ALTER TABLE `inventory_transactions` DISABLE KEYS */;
INSERT INTO `inventory_transactions` VALUES (1,'Hair Shampoo','Stock In',50,'Received from supplier: Beauty Essentials Co.','2025-06-26 21:04:17','2025-06-26 13:04:17'),(2,'Hair Dye','Stock In',20,'Received from supplier: ColorTrend Ltd.','2025-06-26 21:05:37','2025-06-26 13:05:37'),(3,'Facial Cleanser','Stock In',20,'Received from supplier: SalonBasics','2025-06-26 21:09:57','2025-06-26 13:09:57'),(4,'Face Mask','Stock In',25,'Received from supplier: SkinVibe Dist.','2025-06-26 21:10:01','2025-06-26 13:10:01'),(5,'Eyebrow Gel','Stock In',20,'Received from supplier: BeautyTrend Co.','2025-06-27 00:18:22','2025-06-26 16:18:22');
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (15,'Hair Shampoo','','Hair Care',30.00,48,10,'2026-01-01',NULL,1,'In Stock'),(16,'Hair Dye','','Hair Care',50.00,48,10,'2026-06-01',NULL,1,'In Stock'),(17,'Facial Cleanser','','Skin Care',25.00,13,10,'2026-01-01',NULL,1,'In Stock'),(18,'Face Mask','','Skin Care',30.00,18,10,'2026-01-01',NULL,1,'In Stock'),(19,'Eyebrow Gel',NULL,'Makeup',0.00,20,10,NULL,NULL,1,'In Stock');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service_products`
--

LOCK TABLES `service_products` WRITE;
/*!40000 ALTER TABLE `service_products` DISABLE KEYS */;
INSERT INTO `service_products` VALUES (1,19,16,1,'2025-06-26 13:09:10','2025-06-26 13:09:10'),(2,19,15,1,'2025-06-26 13:09:10','2025-06-26 13:09:10'),(3,22,18,1,'2025-06-26 15:23:55','2025-06-26 15:23:55'),(4,22,17,1,'2025-06-26 15:23:55','2025-06-26 15:23:55');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (19,'Deluxe Haircut','Salon',350.00,1,'Premium haircut with styling and scalp massage'),(20,'Spa Manicure','Nail Care',200.00,0,'Luxury manicure with exfoliation and massage'),(21,'Pedicure','Nail Care',250.00,0,'Complete foot care with polish and massage'),(22,'Facial Treatment','Skin Care',400.00,1,'Deep cleansing facial with hydration mask'),(23,'Hair Treatment','Salon',300.00,0,'Nourishing treatment for damaged hair'),(24,'Waxing','Spa Care',150.00,0,'Full-body or targeted waxing service'),(25,'Makeup Application','Makeup',500.00,0,'Professional makeup for events or special occasions'),(26,'Tesing','Testing',900.00,1,'Testing');
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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'Beauty Essentials Co.','Hair Shampoo','Hair Care','555-2001','sales@beautyessentials.com',1,0,'received','2025-06-26 13:02:40','2025-06-26 13:04:17'),(2,'Glam Supplies','Conditioner','Hair Care','555-2002','info@glamsupplies.com',1,30,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(3,'ColorTrend Ltd.','Hair Dye','Hair Care','555-2003','contact@colortrend.com',0,0,'received','2025-06-26 13:02:40','2025-06-26 13:05:37'),(4,'NailGlow Inc.','Nail Polish','Nail Care','555-2004','support@nailglow.com',1,40,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(5,'SkinVibe Dist.','Face Mask','Skin Care','555-2005','sales@skinvibe.com',1,0,'received','2025-06-26 13:02:40','2025-06-26 13:10:01'),(6,'PureLotion Co.','Body Lotion','Skin Care','555-2006','info@purelotion.com',0,15,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(7,'StylePro Supplies','Hair Gel','Hair Care','555-2007','contact@stylepro.com',1,35,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(8,'LipLux Co.','Lip Balm','Lip Care','555-2008','support@liplux.com',1,10,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(9,'SalonBasics','Facial Cleanser','Skin Care','555-2009','sales@salonbasics.com',0,0,'received','2025-06-26 13:02:40','2025-06-26 13:09:57'),(10,'NailArt Supplies','Nail Top Coat','Nail Care','555-2010','info@nailart.com',1,30,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(11,'HairGlow Ltd.','Hair Serum','Hair Care','555-2011','contact@hairglow.com',1,25,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(12,'SpaEssentials','Massage Oil','Spa Care','555-2012','sales@spaessentials.com',0,15,'pending','2025-06-26 13:02:40','2025-06-26 13:02:40'),(13,'BeautyTrend Co.','Eyebrow Gel','Makeup','555-2013','info@beautytrend.com',1,0,'received','2025-06-26 13:02:40','2025-06-26 16:18:22');
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
INSERT INTO `transactions` VALUES ('TXN-20250626-22459','OR-20250626-2276',22,'aw','awdaw','Male','awdwad','Cash - Downpayment (50%)',30.00,120.00,400.00,140.00,'VIP30',NULL,'2025-06-26 23:06:03',1),('TXN-20250626-34407','OR-20250626-3259',22,'Alex','09155273232','Male','Manila','Cash',0.00,0.00,400.00,400.00,'',NULL,'2025-06-26 23:25:44',1),('TXN-20250626-39070','OR-20250626-3758',19,'Allen James','091321312312','Male','Marikina City','Cash',10.00,35.00,350.00,315.00,'WELCOME10',NULL,'2025-06-26 21:31:01',2),('TXN-20250626-48876','OR-20250626-1835',19,'Jhon Arol De Chavez','09283743473','Male','Marikina City','Cash',30.00,105.00,350.00,245.00,'VIP30',NULL,'2025-06-26 21:14:55',1),('TXN-20250626-70246','OR-20250626-4394',22,'awdawdwa','092313231','Male','Marikina City','Cash - Full Payment',0.00,0.00,400.00,400.00,'VIP30',NULL,'2025-06-26 23:10:49',1),('TXN-20250626-83176','OR-20250626-2286',22,'awdawdwa','092313231','Male','Marikina City','Cash - Full Payment',0.00,0.00,400.00,400.00,'',NULL,'2025-06-26 23:06:58',1),('TXN-20250626-86684','OR-20250626-3959',22,'Kyrie','0912313123','Male','Marikina City','Cash',0.00,0.00,400.00,0.00,'',NULL,'2025-06-26 22:57:16',1),('TXN-20250626-94913','OR-20250626-5994',22,'Lebron','02323232323','Male','Marikina City','Cash',0.00,0.00,400.00,0.00,'',NULL,'2025-06-26 22:44:31',1),('TXN-20250626-95496','OR-20250626-4771',22,'Testing','Testing','Male','testing','Cash',0.00,0.00,400.00,400.00,'','2nd session is 6/30/2025','2025-06-26 23:38:28',1),('TXN-20250626-99419','OR-20250626-1367',19,'Nigga','Nigga','Male','Nigga','Cash',30.00,105.00,350.00,245.00,'VIP30','nwidnwandwajdnwadnwajdnwadwkdawkdawdkawdkwadmkwada','2025-06-26 23:51:54',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Juan','juan123','Juan Perez','admin','2025-06-27 02:42:47','2025-06-12 05:23:23','2025-06-26 18:42:46','2025-06-26 22:29:19',58447,NULL,NULL),(2,'Maria','maria123','Maria Lopez','staff','2025-06-26 22:24:55','2025-06-12 05:23:23','2025-06-26 14:24:54','2025-06-17 21:42:50',9018,NULL,NULL);
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

-- Dump completed on 2025-06-27  3:06:12
