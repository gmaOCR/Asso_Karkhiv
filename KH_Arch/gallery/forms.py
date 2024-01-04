from django import forms
from .models import PhotoEvent, PhotoProject

class PhotoEventForm(forms.ModelForm):
    class Meta:
        model = PhotoEvent
        fields = '__all__'  # Ajustez selon les champs que vous souhaitez inclure

class PhotoProjectForm(forms.ModelForm):
    class Meta:
        model = PhotoProject
        fields = '__all__'
