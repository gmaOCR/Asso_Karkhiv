from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=50, default="Example")
    description = models.TextField()
    place = models.CharField(max_length=255)
    date = models.DateField()
    cover = models.ImageField(upload_to='event_covers/', null=True, blank=True)

    def clean(self):
        """Vérifier que la date de l'Event est dans le futur."""
        if self.date and self.date < timezone.now().date():
            raise ValidationError("The date must set in the future")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description
