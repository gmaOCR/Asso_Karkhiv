from django.shortcuts import render
from projects.models import ProjectType


def home_page(request):
    types = ProjectType.choices
    context = {
        'types': types,
    }
    return render(request, 'home/base.html', context)

    