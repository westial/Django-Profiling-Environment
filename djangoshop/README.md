djangoshop
==========

Django root instance hosting different Apps.


Description
-----------

Django framework site part of Django Profiling Environment. Djangoshop is the
component represented by a website where customer goes and clicks on the 
"purchase" button.

There are different Apps hosted here, each one is a different option of this
component. 


Requirements
------------

* Python 2.7.6
* python-dev
* libpcre3
* libpcre3-dev
* Python libraries: Django 1.7.1, django-bootstrap3


Directories
-----------

* app_rdbms: RDBMS App.
* djangoshop: root Django directory.
* etc: configuration files for related services. In this case nginx and uwsgi.
* media: media files directory.
* static: css, javascript, image and other frontend files.
* tags: Django app sharing the tags and filters exclusively.
* vendor: python modules not based on Django.


RDBMS App (app_rdbms)
=====================

This App of this component is the traditional deployment for a website with
database: a frontend and backend based on Django and the MySQL database.

Interesting options for this App benchmarking:

* Website and Database in the same node.
* Website and Database in different node.


Requirements
------------

* MySQL 5.5
* libmysqlclient-dev
* Python libraries: MySQLdb, django-cassandra-engine
	

Database configuration
----------------------

Incremental id is not supported by django model API, you need to set it
manually:

```
ALTER TABLE `app_rdbms_product` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_sale` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_user` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
```

App database tables Structure
-----------------------------

```
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `djangoshop_rdbms`
--

-- --------------------------------------------------------

--
-- Table structure for table `app_rdbms_product`
--

CREATE TABLE IF NOT EXISTS `app_rdbms_product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(90) COLLATE utf8_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `inventory` bigint(20) NOT NULL,
  `created` datetime NOT NULL,
  `modified` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=7 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_rdbms_sale`
--

CREATE TABLE IF NOT EXISTS `app_rdbms_sale` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `app_rdbms_sale_9bea82de` (`product_id`),
  KEY `app_rdbms_sale_e8701ad4` (`user_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2455 ;

-- --------------------------------------------------------

--
-- Table structure for table `app_rdbms_user`
--

CREATE TABLE IF NOT EXISTS `app_rdbms_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(90) COLLATE utf8_unicode_ci NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci AUTO_INCREMENT=2458 ;
```


References
----------

* http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
* http://stackoverflow.com/questions/21669354/rebuild-uwsgi-with-pcre-support


Cassandra App (app_cassandra)
=============================

Deployment consisting on a Django website with a noSQL Cassandra database.


Database Description
--------------------

```
CREATE KEYSPACE djangoshop_cassandra WITH replication = {
  'class': 'SimpleStrategy',
  'replication_factor': '3'
};

USE djangoshop_cassandra;

CREATE TABLE product (
  id uuid,
  date timestamp,
  created timestamp,
  description text,
  image text,
  inventory bigint,
  modified timestamp,
  title text,
  PRIMARY KEY (id, date)
) WITH CLUSTERING ORDER BY (date DESC) AND
  bloom_filter_fp_chance=0.010000 AND
  caching='KEYS_ONLY' AND
  comment='' AND
  dclocal_read_repair_chance=0.000000 AND
  gc_grace_seconds=864000 AND
  index_interval=128 AND
  read_repair_chance=0.100000 AND
  populate_io_cache_on_flush='false' AND
  default_time_to_live=0 AND
  speculative_retry='99.0PERCENTILE' AND
  memtable_flush_period_in_ms=0 AND
  compaction={'class': 'SizeTieredCompactionStrategy'} AND
  compression={'sstable_compression': 'LZ4Compressor'};

CREATE TABLE sale (
  product_id uuid,
  user_email text,
  created timestamp,
  quantity int,
  PRIMARY KEY ((product_id, user_email), created)
) WITH CLUSTERING ORDER BY (created DESC) AND
  bloom_filter_fp_chance=0.010000 AND
  caching='KEYS_ONLY' AND
  comment='' AND
  dclocal_read_repair_chance=0.000000 AND
  gc_grace_seconds=864000 AND
  index_interval=128 AND
  read_repair_chance=0.100000 AND
  populate_io_cache_on_flush='false' AND
  default_time_to_live=0 AND
  speculative_retry='99.0PERCENTILE' AND
  memtable_flush_period_in_ms=0 AND
  compaction={'class': 'SizeTieredCompactionStrategy'} AND
  compression={'sstable_compression': 'LZ4Compressor'};

CREATE TABLE user (
  email text,
  created timestamp,
  PRIMARY KEY (email)
) WITH
  bloom_filter_fp_chance=0.010000 AND
  caching='KEYS_ONLY' AND
  comment='' AND
  dclocal_read_repair_chance=0.000000 AND
  gc_grace_seconds=864000 AND
  index_interval=128 AND
  read_repair_chance=0.100000 AND
  populate_io_cache_on_flush='false' AND
  default_time_to_live=0 AND
  speculative_retry='99.0PERCENTILE' AND
  memtable_flush_period_in_ms=0 AND
  compaction={'class': 'SizeTieredCompactionStrategy'} AND
  compression={'sstable_compression': 'LZ4Compressor'};
```

References
----------

* http://planetcassandra.org/install-cassandra-ova-on-virtualbox/
* http://planetcassandra.org/blog/the-django-cassandra-engine-the-cassandra-backend-for-django/