from django.contrib import admin

from .adminForms import PhotoAdminForm
from .models import Photo


class PhotoAdmin(admin.ModelAdmin):
    form = PhotoAdminForm

    class Media:
        js = ('js/admin.js',)


admin.site.register(Photo, PhotoAdmin)
