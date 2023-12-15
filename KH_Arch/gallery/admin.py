from django.contrib import admin
from .forms import PhotoProject, PhotoEvent, PhotoEventForm, PhotoProjectForm


class PhotoEventAdmin(admin.ModelAdmin):
    form = PhotoEventForm
    # Autres configurations...


class PhotoProjectAdmin(admin.ModelAdmin):
    form = PhotoProjectForm
    # Autres configurations...


admin.site.register(PhotoEvent, PhotoEventAdmin)
admin.site.register(PhotoProject, PhotoProjectAdmin)
