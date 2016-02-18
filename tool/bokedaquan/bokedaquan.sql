/*
Navicat MySQL Data Transfer

Source Server         : conn
Source Server Version : 50160
Source Host           : localhost:3306
Source Database       : bokedaquan

Target Server Type    : MYSQL
Target Server Version : 50160
File Encoding         : 65001

Date: 2016-02-18 16:50:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for kl_boke
-- ----------------------------
DROP TABLE IF EXISTS `kl_boke`;
CREATE TABLE `kl_boke` (
  `blog_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `descr` varchar(255) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `blog_type` varchar(255) DEFAULT NULL,
  `src_url` varchar(255) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for kl_url
-- ----------------------------
DROP TABLE IF EXISTS `kl_url`;
CREATE TABLE `kl_url` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `src_url` varchar(255) DEFAULT NULL,
  `hostname` varchar(255) DEFAULT NULL,
  `update_time` int(11) DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=64510 DEFAULT CHARSET=utf8;
