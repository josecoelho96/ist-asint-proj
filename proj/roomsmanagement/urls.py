from django.conf.urls import url

from . import views

app_name = 'roomsmanagement'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^search$', views.search, name='search'),
    url(r'^checkin$', views.checkin, name='checkin'),
    url(r'^room$', views.room_details, name='room_details'),
    url(r'^get_messages$', views.get_messages, name='get_messages'),
    url(r'^checkout$', views.checkout, name='checkout'),
]
