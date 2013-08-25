from piston.handler import BaseHandler
from django.core.exceptions import *
from PodCasts.models import *

import datetime

class PodCastHandler(BaseHandler):
  allowed_methods = ('GET', 'POST')
  model = PodCast

  # Get
  def read(self, request, PodCast_id = None):
    if PodCast_id:
      podCast = PodCast.objects.get(id=PodCast_id)
      podCast.updateIfReq()
      return podCast
    else:
      return PodCast.objects.all()

  # POST
  def create(self, request):
    podcast_url = request.POST['podcast_url']
    podcast_url = podcast_url.lower().strip()
    (p, created) = PodCast.objects.get_or_create(Link=podcast_url)
    if created:
      p.update(True)
    else:
      p.updateIfReq()
    return p

class ShowHandler(BaseHandler):
  allowed_methods = ('GET',)
  exclude = ('Podcast',)
  model = Show
  extra_fields = ('userInstance',)

  def read(self, request, P_id= None, S_id = None):
    count = -1 
    dtFrom = None
    dtTo = None

    podCast = PodCast.objects.get(id=P_id)
    podCast.updateIfReq()
    
    try:
      if "from" in request.GET:
        dtFrom = datetime.datetime.fromtimestamp(int(request.GET["from"]))
      if "to" in request.GET:
        dtTo   = datetime.datetime.fromtimestamp(int(request.GET["to"]))
      if "count" in request.GET:
        count = int(request.GET["count"])
    except Exception as e:
      pass

    try:
      if S_id:
        return Show.objects.get(id=S_id, Podcast_id = P_id)
      else:
        shows = None
        if dtFrom and dtTo:
          shows = Show.objects.filter(Podcast_id = P_id, PubDate__lte = dtTo, PubDate__gte = dtFrom).order_by('-PubDate')
        elif dtTo:
          shows = Show.objects.filter(Podcast_id = P_id, PubDate__lte = dtTo)
        elif dtFrom:
          shows = Show.objects.filter(Podcast_id = P_id, PubDate__gte = dtFrom)
        else:
          shows = Show.objects.filter(Podcast_id = P_id).order_by('-PubDate')

        if count and count > 0:
          shows = shows[:count]
          
        return shows
    except ObjectDoesNotExist as e:
      return None  

    def userInstance(*args):
      print "HI"

class FavoriteHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'UPDATE', 'DELETE')
  model = Favorite
  exclude = ('User',)

  def read(self, request):
    if request.user.is_authenticated():
      return Favorite.objects.filter(User_id=request.user.id)
    return None

  def create(self, request, P_id):
    if request.user.is_authenticated():
      (f, created) = Favorite.objects.get_or_create(User_id = request.user.id, Podcast_id = P_id)
    return None

  def update(self, request, P_id):
    return None

  def delete(self, request, P_id):
    if request.user.is_authenticated():
      try:
        fav = Favorite.objects.get(User_id=request.user.id, Podcast_id=P_id)
        fav.delete()
      except ObjectDoesNotExist as e:
        pass
    return None


class InstanceHandler(BaseHandler):
  allowed_methods = ('GET', 'POST', 'UPDATE', 'DELETE')
  model = Instance
  exclude = ('User','Show','PodCast')

  def read(self, request, P_id = None, S_id = None):
    if request.user.is_authenticated():
      if P_id != None:
        return Instance.objects.filter(User_id=request.user.id, PodCast_id=P_id)
      if S_id != None:
        return Instance.objects.get(User_id=request.user.id, Show_id=S_id)
      else:
        return Instance.objects.filter(User_id=request.user.id)
    return None
 
  def create(self, request, S_id):
    return None

  def update(self, request, S_id):
    return None

  def delete(self, request, S_id):
    if request.user.is_authenticated():
      try:
        inst = Instance.objects.get(User_id=request.user.id, Show_id=S_id)
        inst.delete()
      except ObjectDoesNotExist as e:
        pass
    return None
