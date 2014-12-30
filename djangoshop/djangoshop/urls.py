from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^rdbms/', include('app_rdbms.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
