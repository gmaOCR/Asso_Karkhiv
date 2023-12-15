import io
from datetime import date

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from .models import PhotoProject, PhotoEvent, File
import os

from projects.models import Project
from events.models import Event

# Obtenez le chemin absolu du fichier actuel (__file__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Remontez dans la hiérarchie des dossiers jusqu'à la racine du projet
# Vous devrez peut-être ajuster le nombre de `os.path.dirname` selon la structure de votre projet
project_root = os.path.dirname(os.path.dirname(current_dir))

# Construisez le chemin relatif
media_root = os.path.join(project_root, 'KH_Arch/media_test')


def create_test_file(name='test_file.txt', content='Test content'):
    file_io = io.BytesIO()
    file_io.write(content.encode())
    file_io.seek(0)
    return ContentFile(file_io.getvalue(), name=name)


def create_test_image(name='test_image.jpg', color='red'):
    image = Image.new('RGB', (100, 100), color=color)
    image_io = io.BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return ContentFile(image_io.getvalue(), name=name)


class CustomTestCase(TestCase):

    def setUp(self):
        # Création d'un projet pour les tests
        self.test_project = Project.objects.create(
            title="Test Project",
            description="A test project",
            place="Test place",
            date=date.today(),
            type="ar"
        )

        self.test_event = Event.objects.create(
            title="Test Event",
            description="A test event",
            place="Test place",
            date=date.today(),
        )

    def tearDown(self):
        # Supprimez tous les fichiers créés dans le dossier media_test
        for root, dirs, files in os.walk(media_root, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

        super().tearDown()


@override_settings(MEDIA_ROOT=media_root)
class PhotoSignalTests(CustomTestCase):

    def test_update_instance_and_file_deletion(self):
        photo = PhotoProject.objects.create(
            description="Test",
            project=self.test_project,
            image=create_test_image('initial_image.jpg')
        )

        # Sauvegarder l'ancien chemin du fichier pour vérifier la suppression plus tard
        old_file_path = photo.image.path
        self.assertTrue(os.path.exists(old_file_path))

        # Mettre à jour l'instance avec une nouvelle image
        new_image = create_test_image('updated_image.jpg', color='blue')
        photo.image.save(new_image.name, new_image, save=True)

        # Vérifier que l'ancien fichier a été supprimé
        self.assertFalse(os.path.exists(old_file_path))
        # Vérifier que le nouveau fichier existe
        self.assertTrue(os.path.exists(photo.image.path))

    def test_photo_project_delete_signal_with_existing_file_on_project_delete(self):
        # Créez une instance de PhotoProject avec une image et une miniature
        photo = PhotoProject.objects.create(
            description="Test PhotoProject",
            project=self.test_project,
            image=create_test_image('existing_image.jpg')
        )
        # Créez une miniature pour la photo
        photo.create_thumbnail()
        photo.save()

        # Capturer les chemins avant de supprimer le projet associé
        image_path = photo.image.path
        thumbnail_path = photo.thumbnail.path

        # Assurez-vous que les fichiers existent
        self.assertTrue(os.path.exists(image_path))
        self.assertTrue(os.path.exists(thumbnail_path))

        # Supprimez le projet associé pour déclencher la suppression en cascade
        self.test_project.delete()

        # Vérifier si les fichiers sont supprimés après la suppression en cascade
        self.assertFalse(os.path.exists(image_path))
        self.assertFalse(os.path.exists(thumbnail_path))


@override_settings(MEDIA_ROOT=media_root)
class PhotoEventSignalTests(CustomTestCase):
    def setUp(self):
        self.test_event = Event.objects.create(
            title="Test Event",
            description="A test event",
            place="Test place",
            date=date.today()
        )

    def test_update_event_instance_and_file_deletion(self):
        photo_event = PhotoEvent.objects.create(
            description="Test Event Photo",
            event=self.test_event,
            image=create_test_image('initial_event_image.jpg')
        )

        # Sauvegarder l'ancien chemin du fichier pour vérifier la suppression plus tard
        old_file_path = photo_event.image.path
        self.assertTrue(os.path.exists(old_file_path))

        # Mettre à jour l'instance avec une nouvelle image
        new_image = create_test_image('updated_event_image.jpg', color='green')
        photo_event.image.save(new_image.name, new_image, save=True)

        # Vérifier que l'ancien fichier a été supprimé
        self.assertFalse(os.path.exists(old_file_path))
        # Vérifier que le nouveau fichier existe
        self.assertTrue(os.path.exists(photo_event.image.path))

    def test_photo_project_delete_signal_with_existing_file_on_project_delete(self):
        # Créez une instance de PhotoProject avec une image et une miniature
        photo = PhotoEvent.objects.create(
            description="Test PhotoEvent",
            event=self.test_event,
            image=create_test_image('existing_image.jpg')
        )
        # Créez une miniature pour la photo
        photo.create_thumbnail()
        photo.save()

        # Capturer les chemins avant de supprimer le projet associé
        image_path = photo.image.path
        thumbnail_path = photo.thumbnail.path

        # Assurez-vous que les fichiers existent
        self.assertTrue(os.path.exists(image_path))
        self.assertTrue(os.path.exists(thumbnail_path))

        # Supprimez le projet associé pour déclencher la suppression en cascade
        self.test_event.delete()

        # Vérifier si les fichiers sont supprimés après la suppression en cascade
        self.assertFalse(os.path.exists(image_path))
        self.assertFalse(os.path.exists(thumbnail_path))


@override_settings(MEDIA_ROOT=media_root)
class ImageReplacementTest(CustomTestCase):

    def test_image_replacement(self):
        # Create an instance of your model with an initial image using the create_test_image method
        initial_image = create_test_image('initial.jpg', color='red')
        photo_project = PhotoProject.objects.create(
            description="Test PhotoProject",
            image=initial_image,
            project=self.test_project  # Reuse the project instance from setUp
        )
        photo_project.save()

        # Verify that the initial image exists
        self.assertTrue(os.path.exists(photo_project.image.path))

        # Replace the image with a new one
        new_image = create_test_image('new.jpg', color='blue')
        photo_project.image.save('new.jpg', new_image, save=True)

        photo_project.refresh_from_db()
        # Verify that the new image has replaced the old one
        self.assertTrue(photo_project.image.name.startswith('photos/new') and photo_project.image.name.endswith('.jpg'))
        self.assertTrue(os.path.exists(photo_project.image.path))

        # Clean up
        photo_project.image.delete(save=False)
        photo_project.delete()


@override_settings(MEDIA_ROOT=media_root)
class ThumbnailReplacementTest(CustomTestCase):

    def test_thumbnail_replacement(self):
        # Créer une instance avec une image initiale
        initial_image = create_test_image('initial.jpg', color='red')
        photo_project = PhotoProject.objects.create(
            description="Test PhotoProject",
            image=initial_image,
            project=self.test_project  # Réutilisez l'instance de projet de setUp
        )

        # Sauvegardez les chemins des fichiers initiaux pour vérifier la suppression plus tard
        initial_image_path = photo_project.image.path
        initial_thumbnail_path = photo_project.thumbnail.path

        # Vérifiez que l'image et la miniature initiales existent
        self.assertTrue(os.path.exists(initial_image_path))
        self.assertTrue(os.path.exists(initial_thumbnail_path))

        # Remplacez l'image par une nouvelle, ce qui devrait également remplacer la miniature
        new_image = create_test_image('new.jpg', color='blue')
        photo_project.image.save('new.jpg', new_image, save=True)

        photo_project.refresh_from_db()

        # Vérifiez que la nouvelle image et la nouvelle miniature ont remplacé les anciennes
        self.assertTrue(photo_project.image.name.startswith('photos/new') and photo_project.image.name.endswith('.jpg'))
        self.assertTrue(os.path.exists(photo_project.image.path))
        self.assertTrue(
            photo_project.thumbnail.name.startswith('thumbnails/new') and photo_project.thumbnail.name.endswith('_thb'
                                                                                                                '.jpg'))
        self.assertTrue(os.path.exists(photo_project.thumbnail.path))

        # Vérifiez que les anciens fichiers ont été supprimés
        self.assertFalse(os.path.exists(initial_image_path))
        self.assertFalse(os.path.exists(initial_thumbnail_path))

        # Nettoyage
        photo_project.image.delete(save=False)
        photo_project.thumbnail.delete(save=False)
        photo_project.delete()


@override_settings(MEDIA_ROOT=media_root)
class FileTests(CustomTestCase):

    def test_file_creation_and_deletion(self):
        # Créer un fichier pour le test
        test_file = create_test_file('test_file.txt', 'Test file content')
        file_instance = File.objects.create(file=test_file)

        # Vérifier que le fichier existe physiquement
        file_path = file_instance.file.path
        self.assertTrue(os.path.exists(file_path))

        # Supprimer l'instance de fichier et vérifier que le fichier physique est supprimé
        file_instance.delete()
        self.assertFalse(os.path.exists(file_path))

    def test_file_update(self):
        # Créer un fichier initial
        initial_file = create_test_file('initial.txt', 'Initial content')
        file_instance = File.objects.create(file=initial_file)

        # Sauvegarder l'ancien chemin du fichier pour vérifier la suppression plus tard
        old_file_path = file_instance.file.path
        self.assertTrue(os.path.exists(old_file_path))

        # Mettre à jour l'instance avec un nouveau fichier
        new_file = create_test_file('updated.txt', 'Updated content')
        file_instance.file.save(new_file.name, new_file, save=True)

        # Vérifier que l'ancien fichier a été supprimé et que le nouveau fichier existe
        self.assertFalse(os.path.exists(old_file_path))
        self.assertTrue(os.path.exists(file_instance.file.path))

        # Nettoyage
        file_instance.file.delete(save=False)


@override_settings(MEDIA_ROOT=media_root)
class SignalTests(CustomTestCase):

    def test_photo_project_delete_signal_with_missing_file(self):
        # Créez une instance de PhotoProject avec une image fictive
        photo = PhotoProject.objects.create(
            description="Test PhotoProject",
            project=self.test_project,
            image=create_test_image('initial_image.jpg')
        )

        # Simulez un fichier manquant en supprimant manuellement le fichier image
        image_path = photo.image.path
        thumbnail_path = photo.thumbnail.path
        os.remove(image_path)
        os.remove(thumbnail_path)

        # Supprimez l'instance et vérifiez que le signal ne lève pas d'exception pour un fichier manquant
        photo.delete()
        self.assertFalse(os.path.exists(image_path))
        self.assertFalse(os.path.exists(thumbnail_path))

    def test_photo_event_delete_signal_with_missing_file(self):
        # Créez une instance de PhotoEvent avec une image fictive
        photo_event = PhotoEvent.objects.create(
            description="Test PhotoEvent",
            event=self.test_event,
            image=create_test_image('event_image.jpg')
        )

        # Simulez un fichier manquant en supprimant manuellement le fichier image
        image_path = photo_event.image.path
        thumbnail_path = photo_event.thumbnail.path
        os.remove(image_path)
        os.remove(thumbnail_path)

        # Supprimez l'instance et vérifiez que le signal ne lève pas d'exception pour un fichier manquant
        photo_event.delete()
        self.assertFalse(os.path.exists(image_path))
        self.assertFalse(os.path.exists(thumbnail_path))

    def test_file_delete_signal_with_missing_file(self):
        # Créez une instance de File avec un fichier fictif
        test_file = create_test_file('test_file.txt', 'Test file content')
        file_instance = File.objects.create(file=test_file)

        # Simulez un fichier manquant en supprimant manuellement le fichier
        file_path = file_instance.file.path
        os.remove(file_path)

        # Supprimez l'instance et vérifiez que le signal ne lève pas d'exception pour un fichier manquant
        file_instance.delete()
        self.assertFalse(os.path.exists(file_path))
