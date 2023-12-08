from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'place', 'date',)


admin.site.register(Project, ProjectAdmin)
