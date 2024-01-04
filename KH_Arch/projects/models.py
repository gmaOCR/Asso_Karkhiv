from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class ProjectType(models.TextChoices):
    ARCHITECTURE = 'ar', 'Architecture'
    URBANISM = 'ur', 'Urbanism'
    RESEARCH = 're', 'Research'
    PUBLICATION = 'pu', 'Publication'
    INTERVIEW = 'in', 'Interview'
    WORKSHOP = 'wo', 'Workshop'


class Project(models.Model):
    title = models.CharField(max_length=50, default="Example")
    description = models.TextField()
    place = models.CharField(max_length=100)
    date = models.DateField()
    type = models.CharField(
        max_length=2,
        choices=ProjectType.choices,
        default=ProjectType.ARCHITECTURE
    )
    thumbnail = models.ForeignKey('gallery.PhotoProject', on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='project_thumbnail')

    @classmethod
    def get_by_type(cls, type_code):
        try:
            type_name = next((name for code, name in ProjectType.choices if code == type_code), None)
        except ObjectDoesNotExist:
            return None, "Project type not found."

        projects = cls.objects.filter(type=type_code).prefetch_related('project_photos')
        return projects, type_name

    def __str__(self):
        return self.title
