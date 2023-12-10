from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=50, default="Example")
    description = models.TextField()
    place = models.CharField(max_length=255)
    date = models.DateField()

    def clean(self):
        """Vérifier que la date de l'Event est dans le futur."""
        if self.date and self.date.date() < timezone.now().date():
            raise ValidationError("La date de l'Event doit être dans le futur.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
