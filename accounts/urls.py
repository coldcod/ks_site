from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name='store_index'), name="login"),
    url(r'^logout/$', views.signout, name="signout"),
    url(r'^settings/$', views.settings, name="settings"),
    url(r'^send_activation_email/$', views.send_activation_email, name="send_activation_email"),
    url(r'^account_activation_sent/$', views.account_activation_sent, name="account_activation_sent"),
    url(r'^activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^xyz/$', views.xyz),
    url(r'^abc/$', views.abc)
]
