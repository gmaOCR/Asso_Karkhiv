from django.contrib import admin
from .models import PhotoProject, PhotoEvent, File


class FileAdmin(admin.ModelAdmin):
    list_display = ("file","project","event",)


class PhotoEventAdmin(admin.ModelAdmin):
    list_display = ("event", "description", "image",)


class PhotoProjectAdmin(admin.ModelAdmin):
    list_display = ("project", "description", "image",)


admin.site.register(File, FileAdmin)
admin.site.register(PhotoEvent, PhotoEventAdmin)
admin.site.register(PhotoProject, PhotoProjectAdmin)
