
from channels.generic.websocket import JsonWebsocketConsumer

from .models import Player
from .handlers import *


class PlayerConsumer(JsonWebsocketConsumer):
    def connect(self):
        ip_address = self.scope['client'][0]
        print("ip_address", ip_address)
        # Get the player's UUID
        uuid = self.scope['url_route']['kwargs']['uuid']
        # Try to get an existing Player
        player = Player.objects.filter(uuid=uuid).first()
        if player is not None:
            self.accept()
            # Update the channel and online fields of the Player
            player.channel = self.channel_name
            player.online = True
            player.save()

    def disconnect(self, close_code):
        # Get the player's UUID
        uuid = self.scope['url_route']['kwargs']['uuid']
        # Try to get an existing Player
        player = Player.objects.filter(uuid=uuid).first()
        if player is not None and player.online:
            # Update the channel and online fields of the Player
            player.channel = ""
            player.online = False
            player.save()

    def receive_json(self, content, **kwargs):
        # Get the player's UUID
        uuid = self.scope['url_route']['kwargs']['uuid']
        if content["type"] == "screenshot":
            handle_player_screenshot(player_uuid=uuid, content=content)
        if content["type"] == "form":
            handle_player_form(player_uuid=uuid, content=content)

    def player_message(self, event):
        print("PlayerMessage :", event["message"])
        self.send_json(event["message"])

    def player_activation(self, event):
        self.send_json({"type": "activation", "activation": event["activation"]})

    def player_playlist(self, event):
        self.send_json({"type": "playlist", "playlist": event["playlist"]})

    def player_telemetry(self, event):
        self.send_json({"type": "telemetry"})

    def player_screenshot(self, event):
        self.send_json({"type": "screenshot", "screenshot": ""})

    def player_image(self, event):
        self.send_json({"type": "image", "image": event["image"]["list"], "duration": event["image"]["duration"]})
