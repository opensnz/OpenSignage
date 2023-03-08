from django.urls import path
from . import views

urlpatterns = [
    path("new", views.new_player, name='new_player_link'),
    path('add', views.add_player, name='add_player_url'),
    path('msg', views.msg_player, name='msg_player_url'),
    path('playlist', views.playlist_to_player, name='playlist_to_player'),
    path('image', views.image_to_player, name='image_to_player'),
]
