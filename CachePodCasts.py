#!/usr/bin/python

import os

from django.core.management import setup_environ
from PodCastSite import settings

setup_environ(settings)

from django.core.files.storage import default_storage
from PodCasts.models import Show,PodCast

def getShow(s):
  url = s.MediaURL
  fileName = s.getAudioFileName() 
  save_path = default_storage.path(fileName)
  if not os.path.isfile(save_path):
    downloadTo(url, save_path)
    s.AudioFile.name = fileName
    s.save()

def downloadTo(url, save_path):
  print save_path
  pid = os.fork()
  if pid == 0: 
    os.execlp("curl", "curl", url, "-o", save_path, "--create-dirs", "-L", "-s")
  print os.wait()


for p in PodCast.objects.all():
  p.update()
  url = p.ImageLink
  fileName = p.getImageFileName()
  save_path = default_storage.path(fileName)
  if not os.path.isfile(save_path):
    downloadTo(url, save_path)
    p.CoverImage.name = fileName
    p.save()

#shows = Show.objects.all()
#for s in shows:
#  getShow(s)
