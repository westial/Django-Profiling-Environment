Report information
==================

Report name: local_2014-12-29_12.35


Description
-----------

The configuration of the environment:

* djangoshop - RDBMS App. Website and database in the same node.
* profilerclient and djangoshop in the same node, my personal computer.


Execution
---------

```
python profilerclient.py \
    -t http://localhost:8000/rdbms \
    -o reports/local_2014-12-29_12.35/report.csv \ 
    -r 10
```

Files
-----

* report.csv: Report results.
* cpuinfo.txt: output after command `cat /proc/cpuinfo` on the unique node.
* meminfo.txt: output after command `cat /proc/meminfo` on the unique node.
* lscpu.txt: output after command `lscpu` on the unique node.