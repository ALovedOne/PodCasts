from django.conf.urls import patterns, url, include

from rest_framework.views import APIView
from rest_framework.response import Response

class Login(APIView):
  def get(self, request, format = None):
    return Response("HI")

urlpatterns = patterns('',
  url(r'^login/', Login.as_view()),
)
