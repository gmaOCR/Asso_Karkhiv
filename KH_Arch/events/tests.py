import os

from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Event
from gallery.models import Photo, File
from datetime import datetime, timedelta
import io


class EventSignalTests(TestCase):

    def setUp(self):
        # Création d'une image en mémoire pour les tests
        image = Image.new('RGB', (100, 100), color='blue')
        image_file = io.BytesIO()
        image.save(image_file, format='PNG')
        image_file.name = 'test_event_image.png'
        image_file.seek(0)

        # Création d'un événement futur pour les tests
        future_date = datetime.now() + timedelta(days=10)
        self.event = Event.objects.create(
            title='Test Event',
            date=future_date
        )

        # Ajout d'une photo de test liée à l'événement
        self.photo = Photo.objects.create(
            description='Test Event Photo',
            content_object=self.event,
            image=SimpleUploadedFile(image_file.name, image_file.getvalue(), content_type='image/png')
        )

        # Ajout d'un fichier de test lié à l'événement
        self.file = File.objects.create(
            file=SimpleUploadedFile('test_event_file.jpg', b'content'),
            event=self.event
        )

    def test_event_deletion_cascades_to_photo_and_file(self):
        # Enregistrer les chemins des fichiers pour vérifier leur suppression
        photo_path = self.photo.image.path
        file_path = self.file.file.path

        # Supprimer l'événement
        self.event.delete()
        print(self.event)
        print(self.file.file.path)
        # Vérifier que la photo et le fichier ont été supprimés
        self.assertFalse(Photo.objects.filter(id=self.photo.id).exists())
        self.assertFalse(File.objects.filter(id=self.file.id).exists())

        # Vérifier que les fichiers physiques ont été supprimés
        self.assertFalse(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(file_path))

    def tearDown(self):
        # Nettoyage après chaque test (si nécessaire)
        pass
