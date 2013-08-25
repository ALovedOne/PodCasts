from django.conf.urls import patterns, url, include
from piston.resource import Resource
from PodCasts.api.handlers import *

PodCast_handler = Resource(PodCastHandler)
Show_handler    = Resource(ShowHandler)
Favorite_handler = Resource(FavoriteHandler)
Instance_handler = Resource(InstanceHandler)

urlpatterns = patterns('',
  url(r'^podcast/$',                      PodCast_handler),
  url(r'^podcast/(?P<PodCast_id>\d+)/$',  PodCast_handler),

  url(r'^podcast/(?P<P_id>\d+)/all/$',           Show_handler),
  url(r'^podcast/(?P<P_id>\d+)/(?P<S_id>\d+)/$', Show_handler),

  url(r'^favorite/$',               Favorite_handler),
  url(r'^favorite/(?P<P_id>\d+)/$', Favorite_handler),

  url(r'^instance/$',               Instance_handler),
  url(r'^instance/podcast/(?P<P_id>\d+)/$', Instance_handler),
  url(r'^instance/show/(?P<S_id>\d+)/$', Instance_handler),
)
