from django.contrib import admin
from django.contrib.auth.models import Group

from .adminForms import CustomUserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = CustomUserChangeForm
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_member')


admin.register(UserAdmin)
admin.site.unregister(Group)