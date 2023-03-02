import json

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import viewsets

from .forms import MediaForm
from .models import Media
from .serializers import MediaSerializer


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


# View for rendering the Media upload form
def upload_media(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            # Generate a unique URL for download based on the media id
            media = form.save(commit=False)
            media.save()
            content = {"media": MediaSerializer(media).data}
            return HttpResponse(content=json.dumps(content), content_type='application/json')
        else:
            return HttpResponseBadRequest()  # Return HTTP "Bad Request" response
    else:
        form = MediaForm()
    return render(request, 'upload_media.html', {'form': form})


# View for downloading a media file
def download_media(request, uuid):
    media = get_object_or_404(Media, uuid=uuid)
    file = media.file
    response = HttpResponse(file, content_type='application/force-download')
    # Use the 'filename' field and the file extension to set the file name
    response['Content-Disposition'] = f'attachment; filename="{media.uuid}{media.extension}"'
    return response
