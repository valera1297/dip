"""diplom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from server.views import *

router = routers.DefaultRouter()

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include(router.urls)),
                  url(r'^rest-auth/', include('rest_auth.urls')),
                  path('user/', User.as_view()),
                  path('works/', Works.as_view()),
                  path('worksid/', WorksId.as_view()),
                  path('addtheme/', AddTheme.as_view()),
                  path('workstudent/', WorksStudents.as_view()),
                  path('workidstudent/', WorksIdStudent.as_view()),
                  path('assessmentstudent/', AssessmentStudent.as_view()),
                  path('teacherstudent/', ThemeStudentTeacher.as_view()),
                  path('resume/', UserResume.as_view()),
                  path('assessmentteacher/', AssessmentTeacher.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
