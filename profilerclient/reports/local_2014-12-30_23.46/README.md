Report information
==================

* Report name: local_2014-12-30_23.46


Description
-----------

* Development webserver for Django (manage.py runserver).
* 1000 concurrent requests.
* djangoshop - RDBMS App. Website and database in the same node.
* profilerclient and djangoshop in the same node, the development workstation.


Execution
---------

profilerclient version: 0.5.1


```
python profilerclient.py \
    -t http://localhost:8000/rdbms \
    -o reports/local_2014-12-30_23.46/report.csv \ 
    -c 1000
```

Files
-----

* report.csv: Report results.
* nodesinfo.txt: server information.