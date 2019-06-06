from rest_framework import permissions, views
from rest_framework.response import Response

from .models import User as UserModel
from .models import Works as WorksModel
from .models import TeacherWorksPlace as TeacherWorksPlaceModel
from .models import Theme as ThemeModel
from .models import MatchingTheme
from .serializers import User as UserSerializer
from .serializers import Works as WorksSerializer
from .serializers import WorksId as WorksIdSerializer
from .serializers import WorksIdStudent as WorksIdStudentSerializer
from .serializers import TeacherStudent
from .serializers import StudentResume


class User(views.APIView):
    model = UserModel

    def get(self, reqest):
        serializer = UserSerializer(reqest.user)
        return Response(serializer.data)


class Works(views.APIView):
    model = WorksModel

    def get(self, reqest):
        serializer = WorksSerializer(self.model.objects.all(), many=True)
        return Response(serializer.data) if reqest.user.isTeacher else Response('')


class WorksId(views.APIView):
    model = TeacherWorksPlaceModel

    def get(self, reqest):
        qset = self.model.objects.filter(work__id=reqest.GET['id'], teacher=reqest.user)
        if (qset.count() == 0):
            return Response('')
        serializer = WorksIdSerializer(qset[0].Theme.all(), many=True)
        return Response(serializer.data) if reqest.user.isTeacher else Response('')

    def post(self, reqest):
        self.model.objects.create(place=reqest.data['place'],
                                  teacher=reqest.user,
                                  work=WorksModel.objects.get(id=reqest.data['id']))
        return Response('')


class AddTheme(views.APIView):
    model = ThemeModel

    def post(self, reqest):
        qset = TeacherWorksPlaceModel.objects.filter(work__id=reqest.data['id'], teacher=reqest.user)[0]
        print(qset)
        self.model.objects.create(shortDescription=reqest.data['sortDescription'],
                                  fullDescription=reqest.data['fullDescription'],
                                  teacherWorkPlace=qset)
        return Response('')


class WorksStudents(views.APIView):
    model = WorksModel

    def get(self, reqest):
        serializer = WorksSerializer(self.model.objects.filter(group=reqest.user.group), many=True)
        return Response(serializer.data)


class WorksIdStudent(views.APIView):
    model = WorksModel

    def get(self, reqest):
        qset = self.model.objects.filter(id=reqest.GET['id'])
        if (qset.count() == 0):
            return Response('')
        serializer = WorksIdStudentSerializer(qset[0].TeacherWorksPlace.all(), many=True, context={'user': reqest.user})
        return Response(serializer.data)


class AssessmentStudent(views.APIView):
    model = MatchingTheme

    def post(self, reqest):
        assemssement = self.model.objects.get_or_create(student=reqest.user,
                                                        theme=ThemeModel.objects.get(id=reqest.data['id']),
                                                        defaults={'assessmentStudent': reqest.data['assessmentStudent'],
                                                                  'noteTheme': reqest.data['noteTheme']})
        assemssement[0].assessmentStudent = reqest.data['assessmentStudent']
        assemssement[0].noteTheme = reqest.data['noteTheme']
        assemssement[0].save()
        return Response('')


class AssessmentTeacher(views.APIView):
    model = MatchingTheme

    def post(self, reqest):
        temp = self.model.objects.get(id=reqest.data['id'])
        temp.assessmentTeacher = reqest.data['assessmentTeacher']
        temp.save()
        return Response('')


class ThemeStudentTeacher(views.APIView):

    def get(self, reqest):
        return Response(TeacherStudent(MatchingTheme.objects.filter(theme__teacherWorkPlace__teacher=reqest.user),
                                       many=True).data)


class UserResume(views.APIView):
    def post(self, request):
        request.user.resume = request.data['resume']
        request.user.save()
        return Response('')

    def get(self, request):
        return Response(StudentResume(request.user).data)
