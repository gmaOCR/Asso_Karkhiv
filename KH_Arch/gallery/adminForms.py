from django import forms
from django.contrib.contenttypes.models import ContentType

from gallery.models import Photo

from projects.models import Project

from events.models import Event


class PhotoAdminForm(forms.ModelForm):
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(
            model__in=['project', 'event']
        ),
        required=True,
        label="Content type"
    )
    object_id = forms.ChoiceField(
        required=False,
        label="Object ID"
    )

    class Meta:
        model = Photo
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PhotoAdminForm, self).__init__(*args, **kwargs)
        self.fields['object_id'].choices = self.get_object_id_choices()

    def get_object_id_choices(self):
        project_choices = [(obj.id, f"{obj.title} (ID: {obj.id})") for obj in Project.objects.all()]
        event_choices = [(obj.id, f"{obj.title} (ID: {obj.id})") for obj in Event.objects.all()]
        return project_choices + event_choices

    def save(self, commit=True):
        photo = super().save(commit=False)
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']

        if content_type == 'project':
            content_type = ContentType.objects.get_for_model(Project)
        elif content_type == 'event':
            content_type = ContentType.objects.get_for_model(Event)

        photo.content_type = content_type
        photo.object_id = object_id
        if commit:
            photo.save()
        return photo
