from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('products.views',
    url(r'^$', 'all', name='products'),
    url(r'^(?P<slug>[\w-]+)/$', 'single', name='single_product'),
)