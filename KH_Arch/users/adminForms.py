from django import forms
from django.contrib.auth.forms import UserChangeForm


from .models import User


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        # Spécifiez les champs à inclure. Par exemple:
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff', 'is_member',)
