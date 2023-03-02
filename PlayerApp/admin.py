from django.contrib import admin
from .models import Player


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'name', 'description', 'tags', 'activated', 'online', 'created_at',
                    'updated_at', 'passcode']


admin.site.register(Player, PlayerAdmin)
