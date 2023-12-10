import os

from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete, post_delete
from django.dispatch import receiver

from .models import Event
from gallery.models import File, Photo


@receiver(pre_delete, sender=Event)
def delete_files_linked_to_event(instance, **kwargs):
    """Supprimer les fichiers File liés à un Event avant la CASCADE"""
    for file in File.objects.filter(event=instance):
        try:
            if file.file and os.path.isfile(file.file.path):
                os.remove(file.file.path)
            file.delete()
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")


@receiver(post_delete, sender=Event)
def event_delete(instance, **kwargs):
    """Supprimer les Photos de l'Event"""
    event_content_type = ContentType.objects.get_for_model(instance)
    for photo in Photo.objects.filter(content_type=event_content_type, object_id=instance.id):
        if photo.image and os.path.isfile(photo.image.path):
            os.remove(photo.image.path)
        if photo.thumbnail and os.path.isfile(photo.thumbnail.path):
            os.remove(photo.thumbnail.path)
        photo.delete()
