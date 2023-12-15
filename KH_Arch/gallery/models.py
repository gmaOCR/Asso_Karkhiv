import os

from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError, SuspiciousFileOperation
from django.db import models
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from events.models import Event
from projects.models import Project


class BasePhoto(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Vérifier si l'instance est mise à jour (et non nouvellement créée)
        if not self._state.adding:
            old_instance = type(self).objects.get(pk=self.pk)

            # Supprimer l'ancien fichier image si différent du nouveau
            if old_instance.image.name != self.image.name:
                old_instance.image.delete(save=False)

            # Supprimer l'ancienne miniature si elle existe
            if old_instance.thumbnail.name and default_storage.exists(old_instance.thumbnail.name):
                old_instance.thumbnail.delete(save=False)

        # Traitement de l'image et création de la miniature
        try:
            if self.image:
                pil_image = Image.open(self.image)
                if pil_image.mode in ['P', 'RGBA']:
                    pil_image = pil_image.convert('RGB')

                buffer = BytesIO()
                pil_image.save(buffer, format='JPEG')
                self.image = InMemoryUploadedFile(
                    buffer, None, self.image.name, 'image/jpeg', sys.getsizeof(buffer), None
                )

                self.create_thumbnail()

        except (UnidentifiedImageError, SuspiciousFileOperation, OSError) as e:
            # Gérer les erreurs d'ouverture d'image ou d'opérations de fichier suspectes
            print(f"Erreur lors de la manipulation de l'image : {e}")

        super().save(*args, **kwargs)

    def create_thumbnail(self):
        try:
            # Ouvrez l'image originale
            if hasattr(self.image.file, 'path'):
                img = Image.open(self.image.path)
            else:
                self.image.seek(0)
                img_file = BytesIO(self.image.read())
                img_file.seek(0)
                img = Image.open(img_file)

            # Convertissez l'image en mode RGB si nécessaire
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Définissez la taille de la miniature
            output_size = (128, 128)
            img.thumbnail(output_size)

            # Sauvegardez la miniature dans un objet BytesIO
            thumb_io = BytesIO()
            img.save(thumb_io, format='JPEG', quality=85)
            thumb_io.seek(0)

            # Construisez le nom du fichier de la vignette
            thumbnail_name = self._get_thumbnail_name()

            # Créez un nouvel objet InMemoryUploadedFile pour la miniature
            thumbnail_file = InMemoryUploadedFile(
                thumb_io, 'ImageField', thumbnail_name, 'image/jpeg', sys.getsizeof(thumb_io), None
            )

            # Sauvegardez le fichier de la vignette dans le champ thumbnail
            self.thumbnail.save(thumbnail_name, thumbnail_file, save=False)

        except UnidentifiedImageError as e:
            print(f"Erreur lors de la création de la miniature : {e}")

    def _get_thumbnail_name(self):
        # Retirez l'extension du fichier original et ajoutez '_thb'
        base_name = os.path.basename(self.image.name)
        name, ext = os.path.splitext(base_name)
        return f'{name}_thb{ext}'

    def delete(self, *args, **kwargs):
        # Supprimer les fichiers image et miniature s'ils existent
        if self.image:
            self.image.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.description


class PhotoEvent(BasePhoto):
    event = models.ForeignKey(Event, related_name='event_photos', on_delete=models.CASCADE)


class PhotoProject(BasePhoto):
    project = models.ForeignKey(Project, related_name='project_photos', on_delete=models.CASCADE)

    @classmethod
    def get_photos_for_project(cls, project):
        """
        Récupère toutes les photos associées à un projet spécifique.
        """
        return cls.objects.filter(project=project)


class ConcretePhoto(BasePhoto):
    pass


class File(models.Model):
    file = models.FileField(upload_to='files')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='project_files')
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, null=True, blank=True,
                              related_name='event_files')

    def clean(self):
        # Vérifier si à la fois projet et event sont définis ou si aucun des deux n'est défini
        if self.project and self.event:
            raise ValidationError("A File cannot be linked to both a project and an event.")
        if not self.project and not self.event:
            raise ValidationError("A File must be linked to either a project or an event.")

    def save(self, *args, **kwargs):
        self.clean()
        # Vérifier si l'instance est mise à jour et si le fichier a changé
        if not self._state.adding and self.pk:
            old_instance = File.objects.get(pk=self.pk)
            if old_instance.file.name != self.file.name and default_storage.exists(old_instance.file.name):
                old_instance.file.delete(save=False)

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Supprimer le fichier physique si il existe
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
            print(f"Fichier {self.file.path} supprimé.")
        super().delete(*args, **kwargs)

    @classmethod
    def get_files_for_project(cls, project):
        """
        Récupère tous les fichiers associés à un projet spécifique.
        """
        return cls.objects.filter(project=project)
