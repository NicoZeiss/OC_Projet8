"""Here are all urls used in user app"""

from django.conf.urls import url
from . import views


app_name = 'user'

urlpatterns = [
    url(r'^create/$', views.create_user, name="create_user"),
    url(r'^connexion/$', views.connexion, name="connexion"),
    url(r'^logout/$', views.logout_user, name="logout"),
    url(r'^account/$', views.account, name="account"),
]
