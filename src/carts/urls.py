from django.conf import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('carts.views',
    #delete the cart by cart id
    #url(r'^cart/(?P<id>\d+)/$', 'carts.views.remove_from_cart', name='remove_from_cart'),
    #url(r'^cart/(?P<slug>[\w-]+)/$', 'carts.views.add_to_cart', name='add_to_cart'),
    url(r'^$', 'view', name='cart'),
    url(r'^add$', 'add_to_cart'),
)