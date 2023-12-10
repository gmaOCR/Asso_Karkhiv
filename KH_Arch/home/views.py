from django.shortcuts import render

from projects.models import ProjectType


def home_page(request):
    types = ProjectType.choices
    return render(request, 'home/base.html', {'types': types})

    