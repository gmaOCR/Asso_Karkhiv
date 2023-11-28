from django.db import models
from django.conf import settings


class Project(models.Model):
    description = models.TextField()
    place = models.CharField(max_length=150)
    date = models.DateField()

