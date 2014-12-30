Profiler from client
====================

Part of the Django-Profiling-Environment. Other components are mandatory.
Visit https://github.com/westial/Django-Profiling-Environment for more
information.

This python module launches that does the benchmark over djangoshop and records
the results into a csv file.


Description
-----------

Concurrent requests to the djangoshop to purchase a product. Each request
returns a basic report from server side and the client side is monitored too.
The list of returned data:

a) Benchmark description and configuration

      1. concurrent_requests: number of concurrent requests launched at the
         same time with this row referred request.
      2. benchmark_title: short description about the benchmark.

b) Opening page. Reports times recorded from client side:

      1. client_home_elapsed_seconds: elapsed seconds between started request
         and response is received.
      2. client_home_error_msg: error message if exists.
      3. client_home_http_code: response http code.
      4. client_home_result: boolean considering result satisfaction.
      5. client_home_started_time: request starting time stamp.
      6. client_home_stopped_time: received response time stamp.

c) Purchasing on main server. Reports times and performance report on server
   side:

      1. server_buy_cpu_usage: cpu usage percentage in server.
      2. server_buy_elapsed_seconds: elapsed seconds between received request
         and saved database records of purchase.
      3. server_buy_error_msg: error message if exists.
      4. server_buy_memory_usage: memory usage megabytes in server.
      5. server_buy_result: boolean considering result satisfaction.
      6. server_buy_started_time: received request time stamp.
      7. server_buy_stopped_time: saved records time stamp.

d) Purchasing on second server. Reports times and performance report on server
   side for server which optionally hosts the external webservices:

      1. server_rest_cpu_usage: cpu usage percentage in server.
      2. server_rest_elapsed_seconds: elapsed seconds between received request
         and saved database records of purchase.
      3. server_rest_error_msg: error message if exists.
      4. server_rest_memory_usage: memory usage megabytes in server.
      5. server_rest_result: boolean considering result satisfaction.
      6. server_rest_started_time: received request time stamp.
      7. server_rest_stopped_time: saved records time stamp.

e) Purchasing on client. Reports times report from client side:

      1. client_buy_elapsed_seconds: elapsed seconds between started request
         and response is received.
      2. client_buy_error_msg: error message if exists.
      3. client_buy_http_code: response http code.
      4. client_buy_result: boolean considering result satisfaction.
      5. client_buy_started_time: request starting time stamp.
      6. client_buy_stopped_time: received response time stamp.


IMPORTANT: before launching tests
---------------------------------

Sync servers to the same NTP server:

    `$ ntpdate ntp.ubuntu.com`

Disable CSRF protection in Django settings MIDDLEWARE_CLASSES:

    `# 'django.middleware.csrf.CsrfViewMiddleware'`