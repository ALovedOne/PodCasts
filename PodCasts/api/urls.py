from django.conf.urls import patterns, include, url
from viewsets import PodCastViewSet, ShowViewSet, FavoriteViewSet, PodCastShowsViewSet,ShowRetrieveUpdateAPIView

from models import Show
from django.http import HttpResponseRedirect

urlpatterns = patterns('',
  url(r'^podcasts/$',             PodCastViewSet.as_view()),
  url(r'^podcasts/(?P<pk>\d+)/$', PodCastViewSet.as_view()),
  url(r'^podcasts/(?P<pk>\d+)/shows/$', 
                                  PodCastShowsViewSet.as_view(),
                                  name = 'podcast-show-list'),
  url(r'^podcasts/(?P<pk>\d+)/shows/(?P<sk>\d+)/',
                                  PodCastShowsViewSet.as_view()),
  url(r'^favorites/$',            FavoriteViewSet.as_view()),
  url(r'^shows/$',                ShowViewSet.as_view()),
  url(r'^shows/(?P<pk>\d+)/$',    ShowRetrieveUpdateAPIView.as_view(),
                                  name = 'podcast-show-update'),
)

def ShowViewRedirect(request, sk):
  s = Show.objects.get(id = sk)
  return HttpResponseRedirect(reverse('podcast-show-list', args = (s.Podcast.id,)))


