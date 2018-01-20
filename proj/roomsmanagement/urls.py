from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^admin/updatedb$', views.update_db, name='update_db'),
    url(r'^admin/history$', views.history, name='history'),
    url(r'^admin/rooms$', views.occupied_rooms, name='admin_rooms'),      
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^auth$', views.auth, name='auth'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^search$', views.search, name='search'),
    url(r'^checkin$', views.checkin, name='checkin'),
    url(r'^room$', views.room_details, name='room_details'),
    url(r'^checkout$', views.checkout, name='checkout'),
    
    
]
