from django.db import models

class YandexDiskLink(models.Model):
    public_key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.public_key
