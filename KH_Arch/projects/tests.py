import os

from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project
from gallery.models import Photo, File
from datetime import date
import io


class ProjectSignalTests(TestCase):

    def setUp(self):
        # Création d'une image en mémoire
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, format='PNG')
        image_file.name = 'test_image.png'
        image_file.seek(0)

        # Création d'un projet de test
        self.project = Project.objects.create(
            title='Test Project',
            date=date.today()
        )

        # Ajout d'une photo de test
        self.photo = Photo.objects.create(
            description='Test Photo',
            content_object=self.project,
            image=SimpleUploadedFile(image_file.name, image_file.getvalue(), content_type='image/png')
        )

        # Ajout d'un fichier de test
        self.file = File.objects.create(
            file=SimpleUploadedFile('test_file.jpg', b'content'),
            project=self.project
        )
        # print(self.file.project.title)

    def test_project_deletion_cascades_to_photo_and_file(self):
        # Enregistrer les chemins des fichiers pour vérifier leur suppression
        photo_path = self.photo.image.path
        file_path = self.file.file.path
        self.project.delete()
        print(self.file)
        # Vérifier que la photo et le fichier ont été supprimés
        self.assertFalse(Photo.objects.filter(id=self.photo.id).exists())
        self.assertFalse(File.objects.filter(id=self.file.id).exists())

        # Vérifier que les fichiers physiques ont été supprimés
        self.assertFalse(os.path.exists(photo_path))
        self.assertFalse(os.path.exists(file_path))

    def tearDown(self):
        # Nettoyage (si nécessaire)
        pass
