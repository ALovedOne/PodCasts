from django.conf.urls import patterns, include, url
from viewsets import PodCastViewSet, ShowViewSet, FavoriteViewSet

urlpatterns = patterns('',
  url(r'^podcast/$',             PodCastViewSet.as_view({'get':'list'})),
  url(r'^podcast/(?P<pk>\d+)/$', PodCastViewSet.as_view({'get':'retrieve'})),
  url(r'^favorite/$',            FavoriteViewSet.as_view({'get':'list'})),
)
