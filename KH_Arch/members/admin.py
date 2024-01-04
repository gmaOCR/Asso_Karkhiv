from django.contrib import admin
from .models import Member, NonMember
from .adminForms import MemberForm


def list_projects(self, obj):
    return ", ".join([project.title for project in obj.projects.all()])


list_projects.short_description = 'Projects'


class MemberAdmin(admin.ModelAdmin):
    form = MemberForm
    list_display = ('get_user_username', 'get_user_firstname', 'get_user_lastname', 'list_projects')
    filter_horizontal = ('projects',)

    def get_user_username(self, obj):
        return obj.user.username

    get_user_username.short_description = 'Username'

    def get_user_firstname(self, obj):
        return obj.user.first_name

    get_user_firstname.short_description = 'FirstName'

    def get_user_lastname(self, obj):
        return obj.user.last_name

    get_user_lastname.short_description = ' LastName'

    list_projects = list_projects


class NonMemberAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'list_projects')
    filter_horizontal = ('projects',)

    list_projects = list_projects


admin.site.register(Member, MemberAdmin)
admin.site.register(NonMember, NonMemberAdmin)
