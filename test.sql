/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50540
Source Host           : localhost:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50540
File Encoding         : 65001

Date: 2016-01-31 21:41:48
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for kl_article
-- ----------------------------
DROP TABLE IF EXISTS `kl_article`;
CREATE TABLE `kl_article` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `category_id` int(11) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `create_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kl_article
-- ----------------------------
INSERT INTO `kl_article` VALUES ('1', '1', '测试标题', '已经更新', null);
INSERT INTO `kl_article` VALUES ('2', '1', '测试标题', '<html \'\'\'\'\'>', null);

-- ----------------------------
-- Table structure for kl_category
-- ----------------------------
DROP TABLE IF EXISTS `kl_category`;
CREATE TABLE `kl_category` (
  `category_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `create_time` int(11) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=gbk;

-- ----------------------------
-- Records of kl_category
-- ----------------------------
INSERT INTO `kl_category` VALUES ('1', '新闻', null);
