djangoshop
==========

Part of the Django-Profiling-Environment. Other components are mandatory.
Visit https://github.com/westial/Django-Profiling-Environment for more
information.

Traditional deployment for a website with database: a frontend and backend based
on Django and the MySQL database.


Description
-----------

Django framework site part of Django Profiling Environment. Djangoshop is the
component represented by a website where customer goes and clicks on the 
"purchase" button.

There are different Apps hosted here, each one is a different option of this
component. Also one of them works at the same time.


RDBMS shop option
=================

Requirements
------------

* MySQL 5.5
* libmysqlclient-dev
* Python 2.7.6
* python-dev
* libpcre3
* libpcre3-dev
* Python libraries:
** Django 1.7.1
** django-bootstrap3
** MySQLdb
	

Database configuration
----------------------

```
$ mysql -u<user> -p

mysql> CREATE USER 'djangoshop_admz'@'localhost' IDENTIFIED BY '43Erfr_t=12';

mysql> GRANT USAGE ON *.* TO 'djangoshop_admz'@'localhost';

mysql> CREATE DATABASE djangoshop_rdbms;

mysql> GRANT CREATE, DROP, DELETE, INSERT, SELECT, UPDATE, ALTER, INDEX, REFERENCES
    -> ON djangoshop_rdbms.* TO 'djangoshop_admz'@'localhost';
	
mysql> FLUSH PRIVILEGES;

mysql> quit
```


Configuring Django
------------------

```
ALTER TABLE `app_rdbms_product` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_sale` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `app_rdbms_user` MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;
```

REFERENCES
==========

* http://uwsgi-docs.readthedocs.org/en/latest/tutorials/Django_and_nginx.html
* http://stackoverflow.com/questions/21669354/rebuild-uwsgi-with-pcre-support
