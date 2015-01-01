from django.conf.urls import patterns, url
from app_cassandra import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<product_id>\d+)/details/$', views.details, name='details'),
    url(r'^(?P<product_id>\d+)/purchase/$', views.purchase,
        name='purchase'),
    url(r'^(?P<product_id>\d+)/purchase/(?P<profiling>\d?)/$', views.purchase,
        name='profiling_purchase'),
)