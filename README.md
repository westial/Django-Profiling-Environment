Django-Profiling-Environment
============================

Environment with multiple deployment and configuration options for benchmarking.


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

