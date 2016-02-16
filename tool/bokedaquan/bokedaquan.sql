/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : bokedaquan

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2016-02-17 00:23:41
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
-- Records of kl_boke
-- ----------------------------
