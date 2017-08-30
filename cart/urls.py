from django.conf.urls import url
from . import views

# Configure cart urls here

urlpatterns = [
    url(r'^add-to-cart/(?P<pid>[0-9A-Za-z]+-[0-9A-Za-z]{1,20})/$', views.add_to_cart, name='cart-add'),
    url(r'^remove-from-cart/(?P<pid>[0-9A-Za-z]+-[0-9A-Za-z]{1,20})/$', views.remove_from_cart, name='cart-remove'),
    url(r'^$', views.cart, name='cart-info')
]
