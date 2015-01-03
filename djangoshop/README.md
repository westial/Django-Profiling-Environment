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
* static_root: Django admin files.
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

```
$ mysql -u<user> -p

mysql> CREATE USER 'djangoshop_adm'@'localhost' IDENTIFIED BY 'password';

mysql> GRANT USAGE ON *.* TO 'djangoshop_adm'@'localhost';

mysql> CREATE DATABASE djangoshop_rdbms;

mysql> GRANT CREATE, DROP, DELETE, INSERT, SELECT, UPDATE, ALTER, INDEX,
    -> REFERENCES ON djangoshop_rdbms.* TO 'djangoshop_adm'@'localhost';
	
mysql> FLUSH PRIVILEGES;

mysql> quit
```

Incremental id is not supported by django model API, you need to set it
manually:

```
ALTER TABLE `app_rdbms_product` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_sale` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_user` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
```


References
----------

* http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
* http://stackoverflow.com/questions/21669354/rebuild-uwsgi-with-pcre-support



Cassandra App (app_cassandra)
=============================

Deployment consisting on a Django website with a noSQL Cassandra database.


References
----------

* http://planetcassandra.org/blog/the-django-cassandra-engine-the-cassandra-backend-for-django/