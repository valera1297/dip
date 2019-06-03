from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import *


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = (
            (None, {'fields': ('last_name', 'first_name', 'patronymic', 'password', 'group', 'isTeacher')}),
    )


admin.site.register(User, MyUserAdmin)
admin.site.register(Theme)
admin.site.register(Group)
admin.site.register(MatchingTheme)
admin.site.register(Works)
admin.site.register(TeacherWorksPlace)
