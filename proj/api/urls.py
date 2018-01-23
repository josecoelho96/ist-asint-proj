from django.conf.urls import url

from . import views


app_name = 'api'
urlpatterns = [

    url(r'^admin/updatedb$', views.update_db, name='update_db'),
    url(r'^admin/history$', views.history, name='history'),
    url(r'^admin/rooms$', views.admin_rooms_occupancy, name='rooms_occupancy'),
    url(r'^admin/room/(?P<room_id>[0-9]+)$', views.admin_room_details, name='admin_room_details'),
    url(r'^admin/send_message$', views.admin_send_message, name='admin_send_message'),
    url(r'^admin/get_messages/(?P<room_id>[0-9]+)$', views.admin_get_messages, name='admin_get_messages'),

    url(r'^user/search/$', views.search, name='search'),    
    url(r'^user/checkin$', views.checkin, name='checkin'),
    url(r'^user/room$', views.room_details, name='user_room_details'),

    url(r'^user/get_messages$', views.get_messages, name='user_get_messages'),


    url(r'^user/checkout$', views.checkout, name='checkout'),


 ]