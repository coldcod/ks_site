from django.conf.urls import url
from django.contrib.auth import views as auth_views
#from django.core.urlresolvers import reverse
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name='next'), name="login"),
    url(r'^login-seller/$', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name='next'), name="login-seller"),
    url(r'^logout/$', views.signout, name="signout"),
    url(r'^settings/$', views.settings, name="settings"),
    url(r'^send_activation_email/$', views.send_activation_email, name="send_activation_email"),
    url(r'^account_activation_sent/$', views.account_activation_sent, name="account_activation_sent"),
    url(r'^activate/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^seller/$', views.seller, name="seller"),
    url(r'^seller-signup/$', views.signup, name="seller-signup"),
    url(r'^seller-login/$', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_field_name="next"), name="seller-login"),
    #url(r'^to-admin/$', RedirectView.as_view(url=reverse('admin'))),

    url(r'^seller/signup/$', views.seller_signup1, name="seller_signup1"),
    url(r'^seller/signup2/$', views.seller_signup2, name="seller_signup2"),
    url(r'^seller/signup3/$', views.seller_signup3, name="seller_signup3"),
    url(r'^seller/signup4/$', views.seller_signup4, name="seller_signup4"),

    url(r'^xyz/$', views.xyz),
    url(r'^abc/$', views.abc)
]
