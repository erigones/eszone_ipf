from django.conf.urls import patterns, include, url

from service_ipf.eszone_ipf.settings import API_VERSION_PREFIX


urlpatterns = patterns('',
    url(r'^{0}/api_ipf/'.format(API_VERSION_PREFIX), include('api_ipf.urls')),
)
