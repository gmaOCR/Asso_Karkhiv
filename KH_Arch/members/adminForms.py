from django import forms
from django.contrib.auth import get_user_model
from .models import Member

User = get_user_model()


class MemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_member=True),
        required=False
    )

    class Meta:
        model = Member
        fields = '__all__'
