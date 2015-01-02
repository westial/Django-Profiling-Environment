Report information
==================

* Report name: local_2015-01-03_14.50


Description
-----------

* Development webserver for Django (manage.py runserver).
* 1000 concurrent requests first to Cassandra App and after the same to RDBMS
  App.
* djangoshop - RDBMS App. Website and database in the same node.
* djangoshop - RDBMS App. Database in a Virtualbox VM, the Cassandra non
  production OVA for testing purposes only.
* profilerclient and djangoshop in the same node, the development workstation.


Executions
----------

profilerclient version: 0.5.4


```
python profilerclient.py \
    -t http://localhost:8000 \
    -d rdbms \
    -o reports/local_2015-01-03_14.50/report_rdbms.csv \ 
    -c 1000
```


```
python profilerclient.py \
    -t http://localhost:8000 \
    -d cassandra \
    -o reports/local_2015-01-03_14.50/report_cassandra.csv \ 
    -c 1000
```

Files
-----

* report.csv: Report results.
* nodesinfo.txt: server information.


Results summaries
-----------------

Results summary of file "reports/local_2015-01-03_14.50/report_cassandra.csv":

Concurrent:			1000
Failed purchases:	692

Maximum value by field:
	158.589 			for field "client_buy_elapsed_seconds"
	36.8 			for field "server_buy_cpu_usage"
	3263 			for field "server_buy_memory_usage"
	15.742 			for field "server_buy_elapsed_seconds"

Common errors:
	353 found.		INTERNAL SERVER ERROR + No JSON object could be decoded + elapsed_seconds
	339 found.		No JSON object could be decoded + elapsed_seconds

Response http codes:
	692 found.		-100
	0 found.		200
(-100 is the code for unknown errors)

--------------------------------------------------------------------------------

Results summary of file "reports/local_2015-01-03_14.50/report_rdbms.csv":

Concurrent:			1000
Failed purchases:	25

Maximum value by field:
	124.053 			for field "client_buy_elapsed_seconds"
	37.5 			for field "server_buy_cpu_usage"
	3107 			for field "server_buy_memory_usage"
	0.935 			for field "server_buy_elapsed_seconds"

Common errors:
	25 found.		No JSON object could be decoded

Response http codes:
	25 found.		-100
	0 found.		200
(-100 is the code for unknown errors)