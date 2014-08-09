from dajaxice.decorators import dajaxice_register

from PodCasts.models import *

import json

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
   
  show_id = kwargs['show_id']
  show = Show.objects.get(id=show_id)
  ret['url'] = show.MediaURL
  if request.user.is_authenticated():
    user_id = request.user.id
    podcast_id = show.Podcast_id
    (inst, created) = Instance.objects.get_or_create(Show_id=show_id,User_id=user_id, PodCast_id=podcast_id)
    ret['position'] = inst.Position
    ret['done']    = inst.Done
    ret['inst_id'] = inst.id
    if created:
      inst.save()
  return json.dumps(ret);

@dajaxice_register
def updateInstance(request, *args, **kwargs):
  inst_id = kwargs['inst_id']
  user_id = request.user.id
  inst = Instance.objects.get(id = inst_id, User_id = user_id)
  if not request.user.is_authenticated():
    ret['needs_auth'] = True 
  elif inst:
    inst.Position = kwargs['curr_pos'] 
    inst.save()
  return json.dumps(kwargs);


@dajaxice_register
def markComplete(request, *args, **kwargs):
  inst_id = kwargs['inst_id']
  user_id = request.user.id
  inst = Instance.objects.get(id = inst_id, User_id = user_id)
  if not request.user.is_authenticated():
    ret['needs_auth'] = True 
  elif inst:
    inst.Done = True
    inst.save()
  return json.dumps(kwargs);


