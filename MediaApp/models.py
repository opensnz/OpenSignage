
from django.db import models
from backend.settings import SERVER_NAME
import uuid


class Media(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to='media/')
    filename = models.CharField(max_length=255)
    extension = models.CharField(max_length=10, editable=False)
    description = models.TextField(blank=True)
    tags = models.CharField(max_length=255, blank=True)
    link = models.URLField(blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Generate a full URL for the 'link' field
        self.link = f'{SERVER_NAME}/media/download/{self.uuid}'
        # Save the file extension with its original extension
        self.extension = self.file.name[self.file.name.rindex("."):]
        # Save the file with the UUID field and its original extension
        self.file.name = f'{self.uuid}{self.extension}'
        # Split tags to list of tag
        if self.tags is not None and str(self.tags) != '' and str(self.tags)[0] != "[":
            self.tags = str(self.tags).split(',')
            print("Media Splitting..")
        super().save(*args, **kwargs)
