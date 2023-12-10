from django.http import Http404
from django.shortcuts import render
from .models import ProjectType, Project


def project_list_by_type(request, type_code):
    # Vérifie si le type_code est dans ProjectType.choices
    type_name = next((name for code, name in ProjectType.choices if code == type_code), None)
    if type_name is None:
        # Si le type n'est pas trouvé, renvoyez une erreur 404
        raise Http404("Project type not found.")

    # Filtre les projets par le type sélectionné
    projects = Project.objects.filter(type=type_code).prefetch_related('photos', 'files')

    # Incluez également la liste complète des types pour la navbar
    types = ProjectType.choices

    return render(request, 'projects/projects_type.html', {
        'type_name': type_name,
        'types': types,
        'projects': projects
    })
