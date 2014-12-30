Profiler from client
====================

Part of the Django-Profiling-Environment. Other components are mandatory.
Visit https://github.com/westial/Django-Profiling-Environment for more
information.

This python module launches that does the benchmark over djangoshop and records
the results into a csv file.

This tool makes a request to the djangoshop component simulating the "purchase"
click with an special option "profiling" enabled. With this enabled option, the
djangoshop component will returns a JSON formatted response with its own
benchmarking information.


IMPORTANT: before launching tests
---------------------------------

Sync servers to the same NTP server:

    `$ ntpdate ntp.ubuntu.com`

Disable CSRF protection in Django settings MIDDLEWARE_CLASSES:

    `# 'django.middleware.csrf.CsrfViewMiddleware'`