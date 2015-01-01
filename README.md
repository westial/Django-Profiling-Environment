Django-Profiling-Environment
============================

Environment with multiple deployment and configuration options for Django
benchmarking.


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

The basis of this project is providing an environment to benchmark a purchase
action in a simple e-commerce application. In this repository there are various
components and each of them can have different working options.

Hosting all components in the same server is not required, actually 
deploying them in different nodes is an interesting option either to have in 
account.


Components
----------

Inside each component directory there is a Readme file with useful information.


### profilerclient

This python module launches that does the benchmark over djangoshop and records
the results into a csv file.

This tool makes a batch of concurrent requests to the djangoshop component 
simulating the "purchase" click with an special option "profiling" enabled.
With this enabled option, the djangoshop component will returns a JSON formatted
response with its own benchmarking information.


### djangoshop

The Django site where the customer clicks on the purchase button. The list of
products is accessible in this website too.


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


Who could need this environment
-------------------------------

If you have a shop online, based on Django, and you want to know what is the 
best deployment and configuration to allow as most customers and activity as 
possible. This environment could be very useful for you.

