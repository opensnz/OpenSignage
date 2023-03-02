from django.contrib import admin
from .models import Media


class MediaAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'file', 'filename', 'extension', 'description', 'tags', 'link', 'created_at', 'updated_at']


admin.site.register(Media, MediaAdmin)
