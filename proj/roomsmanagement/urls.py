from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^update_db/$', views.update_db),
    url(r'^list_rooms/$', views.list_rooms),
    url(r'^search/$', views.search),
]
