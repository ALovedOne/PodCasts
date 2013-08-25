from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from PodCasts import views
from PodCasts.models import PodCast

import api2

urlpatterns = patterns('',
  url(r'^$',             views.PodCastList,    name='index'),
  url(r'^(?P<pk>\d+)/$', views.PodCastDetails, name='detail'),
  url(r'^create/$',      views.create,         name='create'),
  url(r'^favorite/$',    views.UserFavorites,  name='favorites'),
#  url(r'^api/',          include('PodCasts.api.urls')),
  url(r'^api/', include(api2.urls)),
)
