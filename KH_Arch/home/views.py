from django.utils import timezone

from django.shortcuts import render
from projects.models import ProjectType, Project
from events.models import Event


def home_page(request):
    types = ProjectType.choices
    latest_project = Project.objects.order_by('-date').first()
    upcoming_event = Event.objects.filter(date__gte=timezone.now()).order_by('date').first()

    context = {
        'types': types,
        'latest_project': latest_project,
        'upcoming_event': upcoming_event,
    }
    return render(request, 'home/home.html', context)
