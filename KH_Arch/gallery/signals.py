import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from gallery.models import Photo


@receiver(post_delete, sender=Photo)
def photo_delete(sender, instance, **kwargs):
    # Supprimez le fichier image
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    # Supprimez le fichier miniature
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)
