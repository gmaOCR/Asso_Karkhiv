from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType


def get_content_objects(request):
    content_type_id = request.GET.get('content_type_id')
    content_type = ContentType.objects.get_for_id(int(content_type_id))
    model = content_type.model_class()

    if model:
        objects = model.objects.all()
        data = [{'id': obj.id, 'name': f"{obj.title} (ID: {obj.id})"} for obj in objects]
        return JsonResponse({'objects': data})
    return JsonResponse({'objects': []})