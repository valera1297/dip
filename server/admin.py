from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import *


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    list_display = ('first_name',  'patronymic', 'last_name', 'isTeacher')
    list_filter = ('isTeacher',)

    fieldsets = (
            (None, {'fields': ('last_name', 'first_name', 'patronymic', 'password', 'group', 'isTeacher', 'resume')}),
    )


admin.site.register(User, MyUserAdmin)


def make_student_teache(modeladmin, request, queryset):
    print(queryset)


make_student_teache.short_description = "составить список студентов"


class AdminWorks(admin.ModelAdmin):
    actions = [make_student_teache]
    def change_view(self, request, object_id, extra_context=None):
        extra_context = extra_context or {}
        quer = Works.objects.get(id=object_id)
        mass = Theme.objects.filter(teacherWorkPlace__work=quer)
        print(mass)
        extra_context['mass'] = mass
        return super().change_view(request, object_id, extra_context=extra_context)


admin.site.register(Works, AdminWorks)


class executor(admin.ModelAdmin):
    list_display = ('shortDescription', 'executor')


admin.site.register(Theme, executor)


admin.site.register(Group)
admin.site.register(MatchingTheme)
admin.site.register(TeacherWorksPlace)
