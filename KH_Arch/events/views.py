from django.shortcuts import render
from .models import Event


def events_list(request):
    events = Event.objects.all()

    return render(request, 'events/events.html', {
        'events': events
    })


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)

    return render(request, 'events/event_detail.html', {
        'event': event
    })
