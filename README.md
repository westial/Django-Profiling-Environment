Django-Profiling-Environment
============================

Environment with multiple deployment and configuration options for benchmarking.


Credits
-------

* Jaume Mila Bea <jaume@westial.com>
* Project home: https://github.com/westial/Django-Profiling-Environment


License
-------

BasicBenchmarker is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

BasicBenchmarker is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
BasicBenchmarker. If not, see http://www.gnu.org/licenses/.


Description
-----------

The basis of this project is providing an environment to benchmark a purchase
action in a simple e-commerce application. In this repository there are various
components and each of them can have different working options.

Hosting all components in the same server is not required, actually 
deploying them in different nodes is an interesting option either to have in 
account.


### Components

#### profilerclient

This python module launches that does the benchmark over djangoshop and records
the results into a csv file.

This tool makes a request to the djangoshop component simulating the "purchase"
click with an special option "profiling" enabled. With this enabled option, the
djangoshop component will returns a JSON formatted response with its own
benchmarking information.


#### djangoshop

The Django site where the customer clicks on the purchase button. The list of
products is accessible in this website too.


##### Directories

* app_rdbms: RDBMS App.
* djangoshop: root Django directory.
* etc: configuration files for related services. In this case nginx and uwsgi.
* media: media files directory.
* static: css, javascript, image and other frontend files.
* static_root: Django admin files.
* vendor: python modules not based on Django.


##### djangoshop - RDBMS App

This App of this component is the traditional deployment for a website with
database: a frontend and backend based on Django and the MySQL database.

Interesting options for this App benchmarking:

* Website and Database in the same node.
* Website and Database in different node.


##### djangoshop - Cassandra App

--> In construction <--


Who could need this environment
-------------------------------

If you have a shop online, based on Django, and you want to know what is the 
best deployment and configuration to allow as most customers and activity as 
possible. This environment could be very useful for you.

