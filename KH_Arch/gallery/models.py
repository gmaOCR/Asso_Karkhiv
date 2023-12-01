import os

from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Photo(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', editable=False)

    def save(self, *args, **kwargs):
        # Si l'image est déjà sauvegardée et que le chemin est accessible, créez le thumbnail
        if self.image and hasattr(self.image, 'path'):
            self.create_thumbnail()

        # Appelez la méthode save() du parent pour sauvegarder l'instance de Photo
        super().save(*args, **kwargs)

    def create_thumbnail(self):
        # Ouvrez l'image originale
        if hasattr(self.image.file, 'path'):
            img = Image.open(self.image.path)
        else:
            # Si le fichier est en mémoire (par exemple, lors de l'upload), utilisez directement
            img = Image.open(BytesIO(self.image.read()))

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

    def _get_thumbnail_name(self):
        # Retirez l'extension du fichier original et ajoutez '_thb'
        base_name = os.path.basename(self.image.name)
        name, ext = os.path.splitext(base_name)
        return f'{name}_thb{ext}'

    def __str__(self):
        return self.description
