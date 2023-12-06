from django.shortcuts import render

from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType


def get_content_objects(request):
    """
   Renvoi
    """
    content_type_id = request.GET.get('content_type_id')
    if content_type_id:
        content_type = ContentType.objects.get_for_id(content_type_id)
        objects = content_type.model_class().objects.all()
        return JsonResponse({
            'objects': [{'id': obj.id, 'name': str(obj)} for obj in objects]
        })
    return JsonResponse({'objects': []})
