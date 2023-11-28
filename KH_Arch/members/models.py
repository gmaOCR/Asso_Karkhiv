from django.db import models
from django.conf import settings


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    biography = models.TextField()
    projects = models.ManyToManyField('Project')
