import os

from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PhotoEvent, PhotoProject, File


@receiver(pre_delete, sender=PhotoProject)
def delete_photo_files(instance, **kwargs):
    # Supprimez le fichier image associé s'il existe
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    # Supprimez le fichier miniature associé s'il existe
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)


@receiver(pre_delete, sender=PhotoEvent)
def delete_photo_files(instance, **kwargs):
    # Supprimez le fichier image associé s'il existe
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
    # Supprimez le fichier miniature associé s'il existe
    if instance.thumbnail and os.path.isfile(instance.thumbnail.path):
        os.remove(instance.thumbnail.path)


@receiver(pre_delete, sender=File)
def delete_file_on_delete(instance, **kwargs):
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)