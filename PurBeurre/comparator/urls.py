from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.listing),
	url(r'^search/$', views.search),
]