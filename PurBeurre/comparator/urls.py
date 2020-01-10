from django.conf.urls import url
from . import views

app_name = 'comparator'

urlpatterns = [
	url(r'^search/$', views.search, name="search"),
	url(r'^(?P<bar_code>[0-9]+)/$', views.detail, name="detail"),
	url(r'^substitute/$', views.substitute, name="substitute"),
	url(r'^save_sub/$', views.save_sub, name="save_sub"),
	url(r'^favourites/$', views.favourites, name="favourites"),
]