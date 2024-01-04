from django.contrib import admin
from .models import Project
from gallery.models import PhotoEvent, PhotoProject, File
from .adminForms import ProjectAdminForm


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'place', 'date', 'get_photos', 'get_files')
    form = ProjectAdminForm

    def get_photos(self, obj):
        photos = PhotoProject.objects.filter(project=obj)
        return ", ".join([photo.description for photo in photos])

    get_photos.short_description = 'Photos'

    def get_files(self, obj):
        files = File.objects.filter(project=obj)
        return ", ".join([file.file.name for file in files])

    get_files.short_description = 'Files'


admin.site.register(Project, ProjectAdmin)
