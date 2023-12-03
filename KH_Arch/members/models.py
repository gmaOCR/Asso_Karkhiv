from django.db import models
from django.conf import settings


def user_photo_upload_filename(instance):
    last_name_upper = instance.user.last_name.upper()
    return f'member_photos/{instance.user.first_name}_{last_name_upper}'


class Member(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_photo_upload_filename, blank=True)
    biography = models.TextField()
    projects = models.ManyToManyField('projects.Project', related_name="members", blank=True)


