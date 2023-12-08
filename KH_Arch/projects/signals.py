from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from projects.models import Project
from gallery.models import Photo, File
import os


@receiver(post_delete, sender=Project)
def project_delete(instance, **kwargs):
    """Supprimer les Photos du projet"""
    # Récupérer le ContentType pour le modèle Project
    project_content_type = ContentType.objects.get_for_model(instance)
    # Supprimer toutes les photos associées au projet
    for photo in Photo.objects.filter(content_type=project_content_type, object_id=instance.id):
        if photo.image and os.path.isfile(photo.image.path):
            os.remove(photo.image.path)
        if photo.thumbnail and os.path.isfile(photo.thumbnail.path):
            os.remove(photo.thumbnail.path)
        photo.delete()


@receiver(pre_delete, sender=Project)
def delete_files_linked_to_project(sender, instance, **kwargs):
    """Supprimer les fichiers File avant la CASCADE"""
    # Récupérer tous les objets File liés au projet qui va être supprimé
    files = File.objects.filter(project=instance)

    # Supprimer les fichiers physiques associés
    for file in File.objects.filter(project=instance):
        try:
            if file.file and os.path.isfile(file.file.path):
                os.remove(file.file.path)
            file.delete()
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")
