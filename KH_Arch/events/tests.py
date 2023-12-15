import os

from PIL import Image
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Event
from gallery.models import PhotoEvent, PhotoProject, File
from datetime import datetime, timedelta
import io



