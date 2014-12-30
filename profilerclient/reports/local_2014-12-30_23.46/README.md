Report information
==================

* Report name: local_2014-12-30_23.46


Description
-----------

* 1000 concurrent requests.
* djangoshop - RDBMS App. Website and database in the same node.
* profilerclient and djangoshop in the same node, the development workstation.


Execution
---------

profilerclient version: 5.0.1


```
python profilerclient.py \
    -t http://localhost:8000/rdbms \
    -o reports/local_2014-12-30_23.46/report.csv \ 
    -c 1000
```

Files
-----

* report.csv: Report results.
* cpuinfo.txt: output after command `cat /proc/cpuinfo` on the unique node.
* meminfo.txt: output after command `cat /proc/meminfo` on the unique node.
* lscpu.txt: output after command `lscpu` on the unique node.