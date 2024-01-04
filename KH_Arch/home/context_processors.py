from .models import Banner


def banner_context(request):
    banner = Banner.objects.first()  # Ou une autre logique pour sélectionner la bannière
    return {'banner': banner}
