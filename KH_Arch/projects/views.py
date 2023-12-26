from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import  Project, ProjectType
from gallery.models import PhotoProject, File


def project_list_by_type(request, type_code):
    projects, type_name = Project.get_by_type(type_code)

    if type_code not in [code for code, _ in ProjectType.choices]:
        raise Http404("Type de projet invalide")

    if projects is None:
        raise Http404(type_name)

    return render(request, 'projects/projects_type.html', {
        'type_name': type_name,
        'projects': projects
    })


def project_detail(request, type_code, project_id):
    project = get_object_or_404(Project, pk=project_id)
    photos = PhotoProject.get_photos_for_project(project)
    files = File.get_files_for_project(project)

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'photos': photos,
        'files': files
    })
