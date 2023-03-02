
from django.urls import path

from . import views

urlpatterns = [
    path('upload', views.upload_media, name='upload_media_url'),
    path('download/<uuid:uuid>', views.download_media, name='download_link'),
]


