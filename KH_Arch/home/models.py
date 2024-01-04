from django.db import models
from django.conf import settings


class Banner(models.Model):
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return f"Bannière {self.pk}"
