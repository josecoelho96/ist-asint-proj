from django.conf.urls import url

from . import views

app_name = 'admin'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^updatedb$', views.update_db, name='update_db'),
    url(r'^history$', views.history, name='history'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^rooms$', views.room_details, name='room_details'),
    url(r'^send_message$', views.send_message, name='send_message'),
    url(r'^get_messages$', views.get_messages, name='get_messages'),
]
