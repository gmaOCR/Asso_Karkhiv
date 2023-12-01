from django.db import models


class Project(models.Model):
    description = models.TextField()
    place = models.CharField(max_length=100)
    date = models.DateField()
    photos = models.ManyToManyField('gallery.Photo', related_name='projects')

    def __str__(self):
        return self.description
