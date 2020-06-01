from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
import UserActions.views as my_views

app_name = "user"

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^my_login/$', my_views.my_login, name='my_login'),
    url(r'^my_logout/$', my_views.my_logout, name='my_logout'),
    url(r'^admin/', admin.site.urls),

    url(r'account_activation_sent/', my_views.account_activation_sent,
        name='account_activation_sent'),
    url(r'activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
        my_views.activate, name='activate'),
]