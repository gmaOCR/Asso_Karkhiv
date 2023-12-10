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

    def __str__(self):
        return self.description
