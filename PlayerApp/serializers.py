from rest_framework.serializers import ModelSerializer

from .models import Player


class PlayerSerializer(ModelSerializer):
    class Meta:
        model = Player
        fields = ('uuid', 'name', 'description', 'tags', 'activated', 'online', 'created_at', 'updated_at',
                  'passcode', 'channel')
