import os

from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Project, ProjectType
from gallery.models import PhotoEvent, PhotoProject, File
from datetime import date
import io


class ProjectListViewTests(TestCase):
    def setUp(self):
        # Création de projets pour chaque type
        self.project_architecture = Project.objects.create(
            title="Projet Architecture",
            description="Description du projet d'architecture",
            place="Paris",
            date=date.today(),
            type=ProjectType.ARCHITECTURE
        )

        self.project_urbanism = Project.objects.create(
            title="Projet Urbanisme",
            description="Description du projet d'urbanisme",
            place="Lyon",
            date=date.today(),
            type=ProjectType.URBANISM
        )

    def test_project_list_by_valid_type(self):
        # Test pour un type de projet valide
        response = self.client.get(reverse('projects_type', args=['ar']))
        self.assertEqual(response.status_code, 200)
        self.assertIn('projects', response.context)
        self.assertIn('types', response.context)
        self.assertTrue(self.project_architecture in response.context['projects'])

    def test_project_list_by_invalid_type(self):
        # Test pour un type de projet invalide
        response = self.client.get(reverse('projects_type', args=['u3']))
        self.assertEqual(response.status_code, 404)
