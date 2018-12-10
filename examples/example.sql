CREATE database test;

GRANT ALL privileges ON test.* to test@'127.0.0.1' identified by 'test';

use test;

CREATE TABLE `user_account` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL DEFAULT '',
  `nickname` char(36) NOT NULL DEFAULT '',
  `password` char(64) NOT NULL DEFAULT '',
  `salt` char(10) NOT NULL DEFAULT '',
  `must_change_password` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `banned` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `suspended` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `status` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_name` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

