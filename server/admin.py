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
            (None, {'fields': ('last_name', 'first_name', 'patronymic', 'password', 'group', 'isTeacher', 'resume')}),
    )

class AdminWorks(admin.ModelAdmin):
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        quer = Works.objects.get(id=object_id)
        mass = Theme.objects.filter(teacherWorkPlace__work=quer)
        print(mass)
        extra_context['mass'] = mass
        return super().change_view(request, object_id, extra_context=extra_context)


admin.site.register(User, MyUserAdmin)
admin.site.register(Theme)
admin.site.register(Group)
admin.site.register(MatchingTheme)
admin.site.register(Works, AdminWorks)
admin.site.register(TeacherWorksPlace)
