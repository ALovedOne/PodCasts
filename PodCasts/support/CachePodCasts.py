#!/usr/bin/python

from django.core.management import setup_environ
from PodCastSite import settings

setup_environ(settings)

from PodCast.models import Show,PodCast

for s in Show.objects.filter(AudioFile = ""):
  print s.Title
