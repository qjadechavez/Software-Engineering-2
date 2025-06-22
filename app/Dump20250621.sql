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
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (9,38,900,'New','2025-06-14 13:56:12'),(10,38,900,'Updated','2025-06-14 13:56:27'),(11,8,25,'Updated','2025-06-14 15:11:27'),(12,8,24,'Updated','2025-06-14 15:11:50'),(14,40,1000,'New','2025-06-17 23:51:53'),(15,41,300,'New','2025-06-18 01:43:16'),(16,42,10,'New','2025-06-18 01:45:40'),(17,43,10,'New','2025-06-18 01:48:40'),(18,19,90,'Updated','2025-06-18 01:55:27'),(19,43,10,'Updated','2025-06-18 02:03:41'),(20,12,80,'Updated','2025-06-18 02:03:58'),(21,8,24,'Updated','2025-06-20 02:33:49'),(22,7,20,'Updated','2025-06-20 04:17:16');
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
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
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Hydrating Shampoo','Moisturizing shampoo for dry and damaged hair.','Haircare',22.99,200,30,'2026-07-15',NULL,1),(2,'Rosehip Face Oil','Nourishing face oil with rosehip extract for glowing skin.','Skincare',59.99,180,25,'2025-10-20',NULL,1),(3,'Gel Nail Polish Set','Set of 6 vibrant gel polishes for salon-quality nails.','Nail Care',34.99,250,40,'2026-02-10',NULL,1),(4,'Keratin Hair Mask','Deep-conditioning mask for smooth, shiny hair.','Haircare',39.99,150,20,'2026-05-30',NULL,1),(5,'Vitamin C Serum','Antioxidant-rich serum for brighter, youthful skin.','Skincare',89.99,200,30,'2025-12-01',NULL,1),(6,'Lash Extension Kit','Professional kit for applying volume lash extensions.','Lash Services',75.00,60,15,NULL,NULL,1),(7,'Botox Prep Cleanser','Gentle cleanser for pre-Botox skin preparationdwa','Medical Spa',45.00,20,10,'2025-11-15',NULL,0),(8,'Argan Oil Conditioner','Nourishing conditioner with pure argan oil.','Haircare',25.99,24,25,'2024-06-20',NULL,0),(9,'Retinol Night Cream','Anti-aging cream with retinol for overnight repair.','Skincare',79.99,120,20,'2025-09-25',NULL,1),(10,'Nail Strengthener','Fortifying base coat for stronger, healthier nails.','Nail Care',19.99,300,50,'2026-01-15',NULL,1),(11,'Sofwave Skin Gel','Cooling gel for Sofwave skin tightening treatments.','Medical Spa',65.00,15,10,'2025-08-30',NULL,0),(12,'Clip-In Hair Extensions','Premium clip-in extensions for instant length and volume','Haircare',150.00,80,15,'2000-01-01',NULL,1),(13,'Eyebrow Wax Strips','Pre-cut wax strips for precise eyebrow shaping.','Waxing',14.99,400,60,'2025-11-10',NULL,1),(14,'Hyaluronic Acid Serum','Hydrating serum for plump, dewy skin.','Skincare',69.99,160,25,'2025-12-20',NULL,1),(15,'Cuticle Oil Pen','Portable pen for nourishing and softening cuticles.','Nail Care',12.99,500,80,'2026-03-01',NULL,1),(16,'Anti-Dandruff Shampoo','Therapeutic shampoo to reduce flakes and scalp irritation.','Haircare',28.99,140,20,'2026-04-10',NULL,1),(17,'Collagen Face Mask','Sheet mask infused with collagen for skin firmness.','Skincare',49.99,100,15,'2025-10-01',NULL,1),(18,'UV Gel Lamp','Professional UV lamp for curing gel manicures.','Nail Care',89.99,40,10,NULL,NULL,1),(19,'Lash Growth Serum','Serum to promote longer, thicker eyelashes','Lash Services',55.00,90,20,'2025-12-15',NULL,1),(20,'Microneedling Kit','At-home microneedling device for skin rejuvenation.','Medical Spa',120.00,25,5,NULL,NULL,1),(21,'Volumizing Hair Spray','Lightweight spray for added hair volume and hold.','Haircare',18.99,250,40,'2026-02-28',NULL,1),(22,'Charcoal Face Scrub','Exfoliating scrub with charcoal for deep cleansing.','Skincare',35.99,130,20,'2025-11-30',NULL,1),(23,'Nail Art Brush Set','Set of 5 brushes for intricate nail art designs.','Nail Care',29.99,200,30,NULL,NULL,1),(24,'Wax Warmer','Electric warmer for smooth wax application.','Waxing',45.00,50,10,NULL,NULL,1),(25,'Peptide Eye Cream','Anti-aging eye cream to reduce puffiness and wrinkles.','Skincare',65.00,110,15,'2025-09-15',NULL,1),(26,'Hair Color Developer','Peroxide developer for professional hair dyeing.','Haircare',15.99,300,50,'2026-01-25',NULL,1),(27,'Sunscreen Face Lotion','SPF 50 lotion for daily UV protection.','Skincare',39.99,170,25,'2025-08-01',NULL,1),(28,'Nail Polish Remover','Acetone-free remover for gentle polish removal.','Nail Care',9.99,400,60,'2026-03-20',NULL,1),(29,'Eyelash Glue','Waterproof glue for secure lash application.','Lash Services',14.99,350,50,'2025-12-10',NULL,1),(30,'Cooling Aloe Gel','Soothing gel for post-treatment skin relief.','Medical Spa',29.99,10,10,'2025-07-30',NULL,0),(31,'Hair Shine Serum','Lightweight serum for glossy, frizz-free hair.','Haircare',32.99,140,20,'2026-05-15',NULL,1),(32,'Clay Face Mask','Detoxifying clay mask for clearer, smoother skin.','Skincare',44.99,120,15,'2025-10-05',NULL,1),(33,'Manicure Tool Set','Complete set of tools for professional manicures.','Nail Care',24.99,180,30,NULL,NULL,1),(38,'Testing','Testing (Edited)','Testing',90.00,900,500,'2026-06-14',NULL,1),(40,'Pulbo','pulbo by johnsons','Skincare',90.00,1000,900,'2026-06-18',NULL,1),(41,'Gatsby','pampatigas ng buhok','Haircare',5.00,300,100,'2026-06-18',NULL,1),(42,'Clay Face Mask (Gold)','Detoxifying clar mask for clearer, smoother skin','Skincare',50000.00,10,10,'2026-06-18',NULL,1),(43,'Serum','Serum.','Skincare',4000.00,10,10,'2026-06-18',NULL,1);
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `services`
--

LOCK TABLES `services` WRITE;
/*!40000 ALTER TABLE `services` DISABLE KEYS */;
INSERT INTO `services` VALUES (1,'Signature Balayage','Haircare',175.00,1,'Custom hand-painted hair color for a natural, blended look.'),(2,'Deluxe Hydrafacial','Skincare',225.00,1,'Advanced facial with hydration and anti-aging boosters.'),(3,'Acrylic Nail Application','Nail Care',65.00,0,'Full set of durable acrylic nails with custom design.'),(4,'Brazilian Keratin Treatment','Haircare',275.00,1,'Long-lasting treatment for smooth, frizz-free hair.'),(5,'Microdermabrasion','Skincare',150.00,1,'Non-invasive exfoliation for smoother, brighter skin.'),(6,'Lash Lift and Tint','Lash Services',90.00,1,'Curl and darken natural lashes for a dramatic effect.'),(7,'Botox Session','Medical Spa',350.00,0,'Targeted Botox injections to reduce wrinkles.'),(8,'Scalp Detox Treatment','Haircare',80.00,1,'Deep-cleansing scalp therapy to promote healthy hair.'),(9,'Glycolic Chemical Peel','Skincare',185.00,1,'Medical-grade peel for improved skin texture and clarity.'),(10,'Gel Pedicure','Nail Care',55.00,1,'Luxury pedicure with long-lasting gel polish.'),(11,'Laser Skin Rejuvenation','Medical Spa',400.00,0,'Advanced laser treatment for youthful, even-toned skin.'),(12,'Full Body Waxing','Waxing',120.00,1,'Complete body waxing for smooth, hair-free skin.'),(13,'Eyebrow Microblading','Brow Services',300.00,1,'Semi-permanent eyebrow enhancement for perfect shape.');
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
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
INSERT INTO `suppliers` VALUES (1,'GlowEssence Co','Hydrating Facial Cleanser','Skincare','+1-555-101-2021','sales@glowessence.com',1,150,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(2,'LuxeLocks Ltd','Argan Oil Shampoo','Haircare','+1-555-102-2022','info@luxelocks.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(3,'VividBeauty Inc','Matte Lipstick','Cosmetics','+1-555-103-2023','orders@vividbeauty.com',1,200,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(4,'PureSkin Solutions','Vitamin C Serum','Skincare','+1-555-104-2024','contact@pureskin.com',1,80,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(5,'SilkyStrands','Keratin Hair Mask','Haircare','+1-555-105-2025','support@silkystrands.com',1,50,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(6,'NailNova','Gel Nail Polish','Nail Care','+1-555-106-2026','sales@nailnova.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(7,'EcoGlow PH','Bamboo Makeup Brushes','Beauty Tools','+63-917-107-2027','info@ecoglowph.ph',1,30,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(8,'RadiantCharm','Whitening Cream','Skincare','+63-918-108-2028','orders@radiantcharm.ph',1,100,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(10,'LashLuxe','Eyelash Growth Serum','Lash Services','+1-555-110-2030','info@lashluxe.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(11,'GlowTech PH','LED Face Mask','Beauty Devices','+63-919-111-2031','support@glowtechph.ph',1,10,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(12,'BlissfulSkin','Collagen Face Mask','Skincare','+1-555-112-2032','contact@blissfulskin.com',1,90,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(13,'NailArtistry','Nail Art Brush Set','Nail Care','+1-555-113-2033','sales@nailartistry.com',1,60,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(14,'SmoothSilk Co','Body Lotion','Skincare','+63-922-114-2034','info@smoothsilk.ph',1,140,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(15,'ColorVibe','Hair Dye','Haircare','+1-555-115-2035','orders@colorvibe.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(16,'PurelyNatural','Essential Oil Perfume','Fragrance','+63-923-116-2036','sales@purelynatural.ph',1,25,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(17,'GlowWave','Sunscreen SPF 50','Skincare','+1-555-117-2037','support@glowwave.com',1,110,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(18,'LuxeNails','Nail Strengthener','Nail Care','+1-555-118-2038','info@luxenails.com',1,70,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(19,'HerbalHaven','Aloe Vera Gel','Skincare','+63-917-119-2039','contact@herbalhaven.ph',1,80,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(20,'VogueStrands','Hair Spray','Haircare','+1-555-120-2040','sales@voguesstrands.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(21,'ChicCosmetics','Foundation','Cosmetics','+63-918-121-2041','orders@chiccosmetics.ph',1,100,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(22,'DewyGlow PH','Micellar Water','Skincare','+63-919-122-2042','info@dewyglow.ph',1,50,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(23,'LashVibe','Eyelash Glue','Lash Services','+1-555-123-2043','support@lashvibe.com',1,40,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(24,'NailGlow','Nail Polish Remover','Nail Care','+1-555-124-2044','sales@nailglow.com',1,130,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(25,'ZenBeauty','Bath Salts','Bath Products','+63-922-125-2045','contact@zenbeauty.ph',1,60,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(26,'SkinLuxe Co','Anti-Aging Cream','Skincare','+1-555-126-2046','info@skinluxe.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(27,'GlossyLocks','Hair Conditioner','Haircare','+63-923-127-2047','orders@glossylocks.ph',1,90,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(28,'VividLashes','Mascara','Cosmetics','+1-555-128-2048','sales@vividlashes.com',1,70,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(29,'PureGlow PH','Toner','Skincare','+63-917-129-2049','support@pureglowph.ph',1,50,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(30,'NailChic','Manicure Tool Set','Nail Care','+1-555-130-2050','info@nailchic.com',1,40,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(31,'SpaEssence','Clay Face Mask','Skincare','+63-918-131-2051','orders@spaessence.ph',1,100,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(32,'HairGlam','Volumizing Hair Spray','Haircare','+1-555-132-2052','sales@hairglam.com',0,0,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(33,'LuxeGlow','Eye Shadow Palette','Cosmetics','+63-919-133-2053','contact@luxeglow.ph',1,80,'2025-06-20 01:59:55','2025-06-20 01:59:55'),(34,'Testing','Testing','testing','09155288980','wadwa@gmail.com',0,90,'2025-06-20 02:26:16','2025-06-20 02:26:36');
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
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
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Juan','juan123','Juan Perez','admin','2025-06-21 20:20:09','2025-06-12 05:23:23','2025-06-21 12:20:08','2025-06-20 23:12:28',21291),(2,'Maria','maria123','Maria Lopez','staff','2025-06-17 21:40:36','2025-06-12 05:23:23','2025-06-17 13:42:50','2025-06-17 21:42:50',9018);
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

-- Dump completed on 2025-06-21 20:30:27
