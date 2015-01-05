Django-Profiling-Environment
============================

Environment with multiple deployment and configuration options to benchmark 
different Django configurations.


Credits
-------

* Jaume Mila Bea <jaume@westial.com>
* Project home: https://github.com/westial/Django-Profiling-Environment


License
-------

Django-Profiling-Environment is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

Django-Profiling-Environment is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
Django-Profiling-Environment. If not, see http://www.gnu.org/licenses/.


Description
-----------

Are you looking for a multiple scenario environment to improve the performance
for a project based on Django?

The basis of this project is providing an environment to benchmark a purchase
action in a simple e-commerce application. In this repository there are various
components and each of them can have different working options.

Hosting all components in the same server is not required, actually 
deploying them in different nodes is an interesting scenario either to have in 
account.


10 minutes to get ready
-----------------------

Exported OVA from Virtualbox on 2015-01-05.

You can have a simple deployment running after no more than 10 minutes importing
the OVA with all requirements and components ready to use. Basic usage:

1. Download OVA.
2. Import Appliance. Don't reinitialize the MAC address.
3. Configure VM network.
4. If IP of the VM is not 192.168.1.45, reconfigure nginx (djangoshop_nginx.conf).
5. Copy profilerclient module from VM to the host.
6. Restart VM.
7. Run profilerclient from host.

### Download the OVA

http://repositories.westial.com/ova/CentOS-6.6-x86_64-Django-Profiling-Environment.ova


### OVA Description

Installed from CentOS-6.6-x86_64-minimal.iso

Guest Additions NOT installed, fix eth0 up at boot

CentOS Base OVA downloaded from http://virtualboxes.org

Installed Django-Profiling-Environment by git from:
https://github.com/westial/Django-Profiling-Environment


#### Pre-installed into the OVA

* Python 2.7.8
* pip
* uwsgi
* nginx
* cassandra
* MySQL


#### Installed Django Profiling Environment into OVA

Django Profiling Environment Version 0.5.7
djangoshop Component version 0.5.2
djangoshop-Cassandra version 0.5.0
profilerclient version 0.5.6
djangoshop-RDBMS version 1.0.0

Project root: 
/home/djangoshop/www/Django-Profiling-Environment

uwsgi and nginx configuration directory:
/home/djangoshop/www/Django-Profiling-Environment/djangoshop/etc/

Web access to djangoshop:
http://<ip>:8000/rdbms
http://<ip>:8000/cassandra
http://<ip>:8000/admin

If the IP of the machine will be different than 192.168.1.45 update the nginx
host configuration:
/home/djangoshop/www/Django-Profiling-Environment/djangoshop/etc/djangoshop_nginx.conf

Django admin user / password: 
admin / djangoshop

mysql user / password: 
root / reverse

user / password: 
root / reverse


Components
----------

* profilerclient
* djangoshop

Other Readme files with information per component:

* ./djangoshop/README.md
* ./profilerclient/README.md


### profilerclient

This tool makes a batch of concurrent requests to the djangoshop component 
simulating the "purchase" click with an special option "profiling" enabled.
With this enabled option, the djangoshop component will returns a JSON formatted
response with its own benchmarking information.


### djangoshop

The Django site where the customer can see the products and submitting the form
could acquire them.


Recommendations
---------------

Create a directory exclusive for a benchmark against a specific deployment 
configuration and save in the same directory information about the server/s 
involved in the benchmark.

Writing the results to a file as information about the environment is a very
good practice. If you are using linux may be you can use the commands below:

```
$ cat /proc/version
$ lscpu
$ free -m
```

Or all in one command with the output to a file:

`printf "$(cat /proc/version)\n\n$(lscpu)\n\n$(free -m)\n" > outputfile.txt`
