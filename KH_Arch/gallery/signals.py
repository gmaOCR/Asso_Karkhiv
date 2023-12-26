from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import PhotoEvent, PhotoProject, File


def delete_files_on_pre_delete(sender, instance, **kwargs):
    # Pour les modèles PhotoProject et PhotoEvent
    if isinstance(instance, (PhotoProject, PhotoEvent)):
        if instance.image:
            instance.image.delete(save=False)
        if instance.thumbnail:
            instance.thumbnail.delete(save=False)

    # Pour le modèle File
    elif isinstance(instance, File):
        if instance.file:
            instance.file.delete(save=False)


for model in [PhotoProject, PhotoEvent, File]:
    pre_delete.connect(delete_files_on_pre_delete, sender=model)
