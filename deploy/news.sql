CREATE TABLE `news` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `content` text,
  `resource` varchar(255) DEFAULT NULL,
  `publish_datetime` datetime DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_50_resource_publish_date_UNIQUE` (`content`(50),`resource`,`publish_datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
