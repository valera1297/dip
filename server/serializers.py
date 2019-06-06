from rest_framework import serializers

from .models import User as UserModel
from .models import Works as WorksModel
from .models import Group as GroupModel
from .models import TeacherWorksPlace as TeacherWorksPlaceModel
from .models import Theme as ThemeModel
from .models import MatchingTheme


class User(serializers.ModelSerializer):
    groupName = serializers.PrimaryKeyRelatedField(source='group.groupName', read_only=True)

    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'patronymic', 'isTeacher', 'groupName')


class Group(serializers.ModelSerializer):
    class Meta:
        model = GroupModel
        fields = ('groupName',)


class Works(serializers.ModelSerializer):
    groups = Group(source='group', read_only=True, many=True)

    class Meta:
        model = WorksModel
        fields = ('nameWork', 'groups', 'id')


class WorksId(serializers.ModelSerializer):
    assessmentStudent = serializers.SerializerMethodField('_selected', read_only=True)
    executor = serializers.SerializerMethodField('_selected_executor', read_only=True)

    def _selected(self, obj):
        temp = obj.MatchingTheme.filter(student=self.context.get("user"))
        if (temp.exists()):
            return temp[0].assessmentStudent
        else:
            return 0

    def _selected_executor(self, obj):
        if (obj.executor):
            return obj.executor.first_name + ' ' + obj.executor.patronymic + ' ' + obj.executor.last_name + ' ' + obj.executor.group.groupName

    class Meta:
        model = ThemeModel
        fields = ('shortDescription', 'fullDescription', 'executor', 'teacherWorkPlace', 'id', 'assessmentStudent')


class WorksIdStudent(serializers.ModelSerializer):
    first_name = serializers.PrimaryKeyRelatedField(source='teacher.first_name', read_only=True)
    last_name = serializers.PrimaryKeyRelatedField(source='teacher.last_name', read_only=True)
    patronymic = serializers.PrimaryKeyRelatedField(source='teacher.patronymic', read_only=True)
    theme = WorksId(source='Theme', read_only=True, many=True)

    class Meta:
        model = TeacherWorksPlaceModel
        fields = ('first_name', 'last_name', 'patronymic', 'theme', 'id')


class TeacherStudent(serializers.ModelSerializer):
    student_first_name = serializers.PrimaryKeyRelatedField(source='student.first_name', read_only=True)
    student_last_name = serializers.PrimaryKeyRelatedField(source='student.first_name', read_only=True)
    student_patronymic = serializers.PrimaryKeyRelatedField(source='student.patronymic', read_only=True)
    themeShort = serializers.PrimaryKeyRelatedField(source='theme.shortDescription', read_only=True)
    themeFull = serializers.PrimaryKeyRelatedField(source='theme.fullDescription', read_only=True)
    student_group = serializers.PrimaryKeyRelatedField(source='student.group.groupName', read_only=True)
    assessmentTeacher = serializers.SerializerMethodField('_selected', read_only=True)
    resume = serializers.SerializerMethodField('_selected_resume', read_only=True)

    def _selected_resume(self, obj):
        if (obj.student.resume):
            return obj.student.resume.url
        else:
            return 0

    def _selected(self, obj):
        if (obj.assessmentTeacher):
            return obj.assessmentTeacher
        else:
            return 0

    class Meta:
        model = MatchingTheme
        fields = (
        'id', 'assessmentTeacher', 'student_first_name', 'student_last_name', 'student_patronymic', 'noteTheme',
        'themeShort', 'themeFull', 'student_group', 'resume')


class StudentResume(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('resume',)
