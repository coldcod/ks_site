from django.conf.urls import url
from . import views

# Configure Store URLs here.

urlpatterns = [
    url(r'^$', views.index, name="store_index"),
    url(r'^(?P<pid_url>(.*)+)/$', views.product_page, name="product_page")
]
