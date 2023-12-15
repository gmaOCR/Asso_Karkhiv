"""
URL configuration for KH_Arch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from gallery import views as gallery_views
from home import views as home_views
from projects import views as project_views

from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-content-objects/', gallery_views.get_content_objects, name='get-content-objects'),
    path('', home_views.home_page, name='home'),
    path('type/<str:type_code>/', project_views.project_list_by_type, name='projects_type'),
    path('type/<str:type_code>/<int:project_id>/', project_views.project_detail, name='project_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
