from dajaxice.decorators import dajaxice_register

from PodCasts.models import *

import json

@dajaxice_register
def hello(request):
  return json.dumps({'message':'Hello World'})

@dajaxice_register
def addFavorite(request, *args, **kwargs):
  PodCast_id = kwargs['PodCast_id']
  ret = {}
  if not request.user.is_authenticated():
    ret['needs_auth']=True   
  else:
    User_id = request.user.id
    ret['PodCast_id'] = PodCast_id
 
    (fav, created) = Favorite.objects.get_or_create(Podcast_id=PodCast_id, User_id=User_id)
    if created:
      ret['favorite'] = True
    else:
      ret['favorite'] = True
    if 'delete' in kwargs:
      fav.delete()
      ret['favorite'] = False
    else:
      fav.save()
  return json.dumps(ret)

@dajaxice_register
def toggleFavorite(request, *args, **kwargs):
  PodCast_id = kwargs['PodCast_id']
  ret = {}
  if not request.user.is_authenticated():
    ret['needs_auth']=True
  else:
    User_id = request.user.id
    (fav, created) = Favorite.objects.get_or_create(Podcast_id=PodCast_id, User_id=User_id)
    if created:
      ret['favorite'] = True
    else:
      fav.delete()
      ret['favorite'] = False
  return json.dumps(ret)

@dajaxice_register
def loadInstance(request, *args, **kwargs):
  ret = {}
  if not request.user.is_authenticated():
    ret['needs_auth'] = True
  else:
    
  return json.dumps(ret);

def updateInstance(request, *args, **kwargs):
  return ""
