from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^account$', views.account),
	url(r'^connection/$', views.connection),
]