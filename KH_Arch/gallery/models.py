import os

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Photo(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='media/photos/')
    thumbnail = models.ImageField(upload_to='media/thumbnails/', editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        if self.image:
            pil_image = Image.open(self.image)
            if pil_image.mode == 'P':  # Vérifier si l'image est en mode palette
                # Convertir l'image en mode RGB
                pil_image = pil_image.convert('RGB')

                # Sauvegarder l'image convertie dans un objet BytesIO
                buffer = BytesIO()
                pil_image.save(buffer, format='JPEG')
                self.image.save(self.image.name, ContentFile(buffer.getvalue()), save=False)

        # Si l'image est déjà sauvegardée et que le chemin est accessible, créez le thumbnail
        if self.image and hasattr(self.image, 'path'):
            self.create_thumbnail()

        # Appelez la méthode save() du parent pour sauvegarder l'instance de Photo
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Supprimez le fichier image associé s'il existe
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)

        # Supprimez le fichier miniature associé s'il existe
        if self.thumbnail:
            if os.path.isfile(self.thumbnail.path):
                os.remove(self.thumbnail.path)

        # Assurez-vous de supprimer l'instance de modèle après la suppression des fichiers
        super(Photo, self).delete(*args, **kwargs)

    def create_thumbnail(self):
        try:
            # Ouvrez l'image originale
            print(hasattr(self.image.file, 'path'))
            if hasattr(self.image.file, 'path'):
                img = Image.open(self.image.path)
            else:
                self.image.seek(0)
                img_file = BytesIO(self.image.read())
                img_file.seek(0)  # Rembobinez au début du fichier
                img = Image.open(img_file)

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

    def __str__(self):
        return self.description


class File(models.Model):
    file = models.FileField(upload_to='media/files')
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, null=True, blank=True)

    def clean(self):
        # Vérifiez si à la fois projet et event sont définis ou si aucun des deux n'est défini
        if (self.project and self.event) or (not self.project and not self.event):
            raise ValidationError("Cannot be linked to both (event and project)")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.file and os.path.isfile(self.file.path):
            os.remove(self.file.path)
            print(f"Fichier {self.file.path} supprimé.")
        super().delete(*args, **kwargs)
