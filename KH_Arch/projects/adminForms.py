from django import forms
from .models import Project
from gallery.models import PhotoProject


class ProjectAdminForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['thumbnail'].queryset = PhotoProject.objects.filter(project=self.instance)

