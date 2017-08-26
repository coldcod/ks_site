from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name='store_index'), name="login"),
    url(r'^logout/$', views.signout, name="signout"),
    url(r'^settings/$', views.settings, name="settings")
]
