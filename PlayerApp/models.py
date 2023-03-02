import json
import random
import uuid

from django.db import models


def generate_passcode():
    return random.randint(100000, 999999)


class Player(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    activated = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    passcode = models.PositiveIntegerField(default=generate_passcode)
    channel = models.CharField(max_length=255, blank=True)
    system = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Split tags to list of tag
        if self.tags is not None and str(self.tags) != '' and str(self.tags)[0] != "[":
            self.tags = str(self.tags).split(',')
            print("Player Splitting..")
        super().save(*args, **kwargs)

