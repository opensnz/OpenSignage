from django.urls import path
from .consumers import PlayerConsumer

websocket_urlpatterns = [
    path('player/<uuid:uuid>', PlayerConsumer.as_asgi())
]
