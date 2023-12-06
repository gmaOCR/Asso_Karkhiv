from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=50, default="Example")
    description = models.TextField()
    place = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.description
