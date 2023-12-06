from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=50, default="Example")
    description = models.TextField()
    place = models.CharField(max_length=255)
    date = models.DateField()
    photos = models.ManyToManyField('gallery.Photo', related_name='events',
                                    blank=True)  # blank=True permet de ne pas avoir de photos liées

    def __str__(self):
        return self.description
