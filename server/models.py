from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    patronymic = models.CharField(max_length=30)
    isTeacher = models.BooleanField(default=False)
    group = models.ForeignKey('Group', null=True, on_delete=models.CASCADE, blank=True, related_name='Student')
    resume = models.FileField(upload_to="resume", null=True, blank=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' ' + self.patronymic


class Group(models.Model):
    groupName = models.CharField(max_length=30)
    relatedName = models.CharField(max_length=30)

    def __str__(self):
        return self.groupName + ' - ' + self.relatedName


class Works(models.Model):
    nameWork = models.CharField(max_length=100)
    group = models.ManyToManyField('Group', related_name='Works')

    def __str__(self):
        return self.nameWork


class TeacherWorksPlace(models.Model):
    place = models.IntegerField()
    work = models.ForeignKey('Works', on_delete=models.CASCADE, related_name='TeacherWorksPlace')
    teacher = models.ForeignKey('User', on_delete=models.CASCADE, related_name='TeacherWorksPlace')


class Theme(models.Model):
    shortDescription = models.CharField(max_length=255, default='Тема предложенная студентом')
    fullDescription = models.TextField(default='-')
    executor = models.OneToOneField('User', on_delete=models.CASCADE, null=True, blank=True, related_name='Student')
    teacherWorkPlace = models.ForeignKey('TeacherWorksPlace', on_delete=models.CASCADE, related_name='Theme')

    def __str__(self):
        return self.shortDescription


class MatchingTheme(models.Model):
    theme = models.ForeignKey('Theme', on_delete=models.CASCADE, blank=True, related_name='MatchingTheme')
    student = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='MatchingTheme')
    assessmentStudent = models.IntegerField()
    assessmentTeacher = models.IntegerField(default=0)
    noteTheme = models.TextField(default='-')
