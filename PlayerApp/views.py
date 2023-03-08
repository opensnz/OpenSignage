import json
import uuid

from asgiref.sync import async_to_sync
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from MediaApp.models import Media
from MediaApp.serializers import MediaDownloadingSerializer

from .forms import PlayerForm
from .models import Player
from .serializers import PlayerSerializer

from channels.layers import get_channel_layer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


# Generate a new player object to Player client
def new_player(request):
    player = Player()
    player.save()
    content = {"type": "player", "player": PlayerSerializer(player).data}
    return HttpResponse(content=json.dumps(content), content_type='application/json')


# Add a generated player : client add a Player with its passcode
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            try:
                passcode = form.cleaned_data['passcode']
                player = get_object_or_404(Player, passcode=passcode)
                # get_object_or_404(Player, passcode=passcode, activated=False)
                player.activated = True
                player.name = form.cleaned_data['name']
                player.description = form.cleaned_data['description']
                player.tags = form.cleaned_data['tags']
                player.save()
                if player.channel != "":
                    channel_layer = get_channel_layer()
                    player_data = PlayerSerializer(player).data
                    player_data.pop("channel")
                    player_data.pop("online")
                    async_to_sync(channel_layer.send)(str(player.channel),
                                                      {"type": "player.activation",
                                                       "activation": player_data})
                content = {"player": PlayerSerializer(player).data}
                return HttpResponse(content=json.dumps(content), content_type='application/json')
            except:
                return HttpResponseBadRequest()  # Return HTTP "Bad Request" response
        else:
            return HttpResponseBadRequest()  # Return HTTP "Bad Request" response
    else:
        form = PlayerForm()
    return render(request, 'add_player.html', {'form': form})


def msg_player(request):
    uuid_player = "56d83cc9-5471-4568-86c8-bc8e6fca6cad"
    try:
        player = get_object_or_404(Player, uuid=uuid_player)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(str(player.channel),
                                          {"type": "chat.message", "message": {"type": "test", "test": "test!!!!!!!"}})
        content = {"player": PlayerSerializer(player).data}
        return HttpResponse(content=json.dumps(content), content_type='application/json')
    except:
        return HttpResponseBadRequest()  # Return HTTP "Bad Request" response


def playlist_to_player(request):
    try:
        body = json.loads(request.body)
        playlist = []
        for media_uuid in body["playlist"]:
            media = get_object_or_404(Media, uuid=media_uuid)
            playlist.append(MediaDownloadingSerializer(media).data)
        channel_layer = get_channel_layer()
        player = get_object_or_404(Player, uuid=body["player"])
        async_to_sync(channel_layer.send)(str(player.channel),
                                          {"type": "player.playlist", "playlist": playlist})
        return HttpResponse(status=200)
    except:
        return HttpResponseBadRequest()  # Return HTTP "Bad Request" response


def image_to_player(request):
    try:
        body = json.loads(request.body)
        images = []
        for image_uuid in body["images"]:
            media = get_object_or_404(Media, uuid=image_uuid)
            images.append(MediaDownloadingSerializer(media).data)
        channel_layer = get_channel_layer()
        player = get_object_or_404(Player, uuid=body["player"])
        async_to_sync(channel_layer.send)(str(player.channel),
                                          {"type": "player.image", "image": {"list": images,
                                                                             "duration": body["duration"]}})
        return HttpResponse(status=200)
    except:
        return HttpResponseBadRequest()  # Return HTTP "Bad Request" response
