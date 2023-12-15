from .models import ProjectType


def project_types_context(request):
    types = ProjectType.choices
    return {'types': types}
