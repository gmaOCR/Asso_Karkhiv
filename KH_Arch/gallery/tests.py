from pathlib import Path
from unittest import mock

from django.core.files.storage import Storage
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from gallery.models import PhotoProject, PhotoEvent, File
from projects.models import Project
from events.models import Event
from datetime import date

from django.core.files.storage import Storage


class InMemoryStorage(Storage):
    def __init__(self, *args, **kwargs):
        self.files = {}

    def _open(self, name, mode='rb'):
        return self.files.get(name)

    def _save(self, name, content):
        self.files[name] = content
        return name

    def exists(self, name):
        return name in self.files

    def delete(self, name):
        if name in self.files:
            del self.files[name]

    def url(self, name):
        return f'/memory/{name}'

    def path(self, name):
        # Retourne un chemin fictif pour les besoins des tests
        return f"/fake_path/{name}"


@pytest.fixture
def in_memory_storage():
    storage = InMemoryStorage()
    with mock.patch('django.core.files.storage.default_storage._wrapped', new=storage):
        yield storage


@pytest.fixture
def test_project(db):
    return Project.objects.create(
        title="Test Project",
        description="A test project description",
        place="Test Place",
        date=date.today(),
        type="ar"
    )


@pytest.fixture
def test_event(db):
    return Event.objects.create(
        title="Test Event",
        description="A test event description",
        place="Test Place",
        date=date.today()
    )


@pytest.mark.django_db
def test_photo_project_delete_signal_with_existing_file_on_project_delete(test_project, in_memory_storage):
    image_content = b'image_file_content'
    thumbnail_content = b'thumbnail_file_content'
    photo = PhotoProject.objects.create(
        description="Test PhotoProject",
        project=test_project,
        image=SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg"),
        thumbnail=SimpleUploadedFile("test_thumbnail.jpg", thumbnail_content, content_type="image/jpeg")
    )
    assert photo.image.name == "test_image.jpg"
    assert photo.thumbnail.name == "test_thumbnail.jpg"

    test_project.delete()
    assert not in_memory_storage.exists(photo.image.name)
    assert not in_memory_storage.exists(photo.thumbnail.name)


@pytest.mark.django_db
def test_update_event_instance_and_file_deletion(test_event, in_memory_storage):
    initial_image = SimpleUploadedFile("original.jpg", b"original_file_content", content_type="image/jpeg")
    new_image = SimpleUploadedFile("updated.jpg", b"new_file_content", content_type="image/jpeg")

    photo_event = PhotoEvent.objects.create(description="Test Event Photo", event=test_event, image=initial_image)
    photo_event.image.save('updated.jpg', new_image)
    assert photo_event.image.name == "photos/updated.jpg"


@pytest.mark.django_db
def test_file_creation_and_deletion(test_project, in_memory_storage):
    test_file = SimpleUploadedFile("test_file.txt", b"Test file content", content_type="text/plain")
    file_instance = File.objects.create(file=test_file, project=test_project)
    assert in_memory_storage.exists(file_instance.file.name)

    file_instance.delete()
    assert not in_memory_storage.exists(file_instance.file.name)


@pytest.mark.django_db
def test_file_update(test_project, in_memory_storage):
    # Créer un fichier initial simulé
    initial_content = SimpleUploadedFile("initial.txt", b"Initial content", content_type="text/plain")
    file_instance = File.objects.create(
        file=initial_content,
        project=test_project
    )

    # Obtenir le chemin du fichier initial et vérifier qu'il existe
    old_file_path = Path(file_instance.file.path)
    assert in_memory_storage.exists(file_instance.file.name)

    # Créer un nouveau fichier simulé
    updated_content = SimpleUploadedFile("updated.txt", b"Updated content", content_type="text/plain")
    file_instance.file.save(updated_content.name, updated_content, save=True)

    # Obtenir le nouveau chemin du fichier et vérifier qu'il existe
    new_file_path = Path(file_instance.file.path)
    assert in_memory_storage.exists(file_instance.file.name)
    assert new_file_path != old_file_path


@pytest.mark.django_db
def test_photo_project_delete_signal_with_existing_file_on_project_delete(test_project, in_memory_storage):
    # Créez une instance de PhotoProject avec des fichiers image et miniature simulés
    image_content = b'image_file_content'
    thumbnail_content = b'thumbnail_file_content'

    photo = PhotoProject.objects.create(
        description="Test PhotoProject",
        project=test_project,
        image=SimpleUploadedFile("test_image.jpg", image_content, content_type="image/jpeg"),
        thumbnail=SimpleUploadedFile("test_thumbnail.jpg", thumbnail_content, content_type="image/jpeg")
    )

    # Capturez les chemins des fichiers
    image_file_path = Path(photo.image.path)
    thumbnail_file_path = Path(photo.thumbnail.path)

    # Assurez-vous que les fichiers existent
    assert in_memory_storage.exists(photo.image.name)
    assert in_memory_storage.exists(photo.thumbnail.name)

    # Supprimez l'objet photo
    photo.delete()

    # Vérifiez que les fichiers ont été supprimés
    assert not in_memory_storage.exists(photo.image.name)
    assert not in_memory_storage.exists(photo.thumbnail.name)


@pytest.mark.django_db
def test_photo_project_deletion_cascade(test_project, in_memory_storage):
    # Créez une instance de PhotoProject avec un fichier image et une miniature simulés
    image_content = b'image_file_content'
    thumbnail_content = b'thumbnail_file_content'
    photo = PhotoProject.objects.create(
        project=test_project,
        image=SimpleUploadedFile("test_proj_image.jpg", image_content, content_type="image/jpeg"),
        thumbnail=SimpleUploadedFile("test_proj_thumbnail.jpg", thumbnail_content, content_type="image/jpeg")
    )

    # Assurez-vous que les fichiers existent
    assert in_memory_storage.exists(photo.image.name)
    assert in_memory_storage.exists(photo.thumbnail.name)

    # Supprimez l'instance de Project, ce qui devrait déclencher la suppression de PhotoProject en cascade
    test_project.delete()

    # Vérifiez que les fichiers ont été supprimés
    assert not in_memory_storage.exists(photo.image.name)
    assert not in_memory_storage.exists(photo.thumbnail.name)


@pytest.mark.django_db
def test_photo_event_deletion_cascade(test_event, in_memory_storage):
    # Créez une instance de PhotoEvent avec des fichiers image et miniature simulés
    image_content = b'image_file_content'
    thumbnail_content = b'thumbnail_file_content'

    photo_event = PhotoEvent.objects.create(
        event=test_event,
        image=SimpleUploadedFile("test_event_image.jpg", image_content, content_type="image/jpeg"),
        thumbnail=SimpleUploadedFile("test_event_thumbnail.jpg", thumbnail_content, content_type="image/jpeg")
    )

    # Assurez-vous que les fichiers existent
    assert in_memory_storage.exists(photo_event.image.name)
    assert in_memory_storage.exists(photo_event.thumbnail.name)

    # Supprimez l'instance de Event, ce qui devrait déclencher la suppression de PhotoEvent en cascade
    test_event.delete()

    # Vérifiez que les fichiers ont été supprimés
    assert not in_memory_storage.exists(photo_event.image.name)
    assert not in_memory_storage.exists(photo_event.thumbnail.name)


@pytest.mark.django_db
def test_file_deletion_cascade(test_project, in_memory_storage):
    # Créez une instance de File avec un fichier simulé associé à test_project
    file_content = b'Some file content'

    file_instance = File.objects.create(
        project=test_project,
        file=SimpleUploadedFile("test_proj_file.txt", file_content, content_type="text/plain")
    )

    # Associez l'objet File à test_project
    file_instance.project = test_project
    file_instance.save()

    # Assurez-vous que le fichier existe
    assert in_memory_storage.exists(file_instance.file.name)

    # Supprimez l'instance de Project, ce qui devrait déclencher la suppression de File en cascade
    test_project.delete()

    # Vérifiez que le fichier a été supprimé
    assert not in_memory_storage.exists(file_instance.file.name)


@pytest.mark.django_db
def test_file_instance_deletion_triggers_file_deletion(in_memory_storage, test_project):
    # Créer une instance de File avec un fichier associé à un projet
    file_content = b'Some file content'
    file_instance = File.objects.create(
        project=test_project,
        file=SimpleUploadedFile("test_file.txt", file_content, content_type="text/plain")
    )

    # Assurez-vous que le fichier existe initialement
    assert in_memory_storage.exists(file_instance.file.name)

    # Supprimer l'instance de File
    file_instance.delete()

    # Vérifier que le fichier associé n'existe plus
    assert not in_memory_storage.exists(file_instance.file.name)
