from rest_framework.serializers import ModelSerializer

from .models import Media


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ('uuid', 'filename', 'extension', 'link', 'description', 'tags', 'created_at', 'updated_at')


class MediaDownloadingSerializer(ModelSerializer):
    class Meta:
        model = Media
        fields = ('uuid', 'extension', 'link')

