from unittest import mock
from django.core.files.storage import Storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse
import pytest
from PIL import Image
from io import BytesIO
from .models import Project
from gallery.models import PhotoProject, File
from datetime import date


class InMemoryStorage(Storage):
    files = {}

    def _open(self, name, mode='rb'):
        return BytesIO(self.files[name])

    def _save(self, name, content):
        self.files[name] = content.read()
        return name

    def exists(self, name):
        return name in self.files

    def delete(self, name):
        del self.files[name]

    def url(self, name):
        return f'/memory/{name}'

    def path(self, name):
        return f'/fake_path/{name}'


@pytest.fixture
def in_memory_storage():
    with mock.patch('django.core.files.storage.default_storage._wrapped', new_callable=lambda: InMemoryStorage()):
        yield


def create_test_image(name='test_image.jpg', color='red', size=(100, 100)):
    image = Image.new('RGB', size, color=color)
    buffer = BytesIO()
    image.save(buffer, format='JPEG')
    buffer.seek(0)
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/jpeg')


@pytest.mark.django_db
def test_project_list_by_valid_type(in_memory_storage):
    project = Project.objects.create(
        title="Projet de Test", description="Description du projet",
        place="Lieu du projet", date=date.today(), type="ar"
    )
    test_image = create_test_image("test_image.jpg")
    PhotoProject.objects.create(project=project, image=test_image)

    client = Client()
    response = client.get(reverse('projects_type', args=['ar']))
    assert response.status_code == 200
    assert 'projects' in response.context
    assert project in response.context['projects']


@pytest.mark.django_db
def test_project_detail_view_with_existing_project(in_memory_storage):
    project = Project.objects.create(
        title="Projet de Test", description="Description du projet",
        place="Lieu du projet", date=date.today(), type="ar"
    )
    test_image = create_test_image("test_image.jpg")
    photo = PhotoProject.objects.create(project=project, image=test_image)

    client = Client()
    url = reverse('project_detail', args=[project.type, project.id])
    response = client.get(url)
    assert response.status_code == 200
    assert project.title in response.content.decode()
    assert photo.thumbnail.url in response.content.decode()
