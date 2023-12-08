from django.contrib import admin

from .adminForms import PhotoAdminForm
from .models import Photo, File


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('description', 'image', 'content_type', 'content_object',)
    form = PhotoAdminForm

    class Media:
        js = ('js/admin.js',)


class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'project', 'event',)


admin.site.register(Photo, PhotoAdmin)
admin.site.register(File, FileAdmin)
