from django.conf.urls import patterns, url
from django.views.generic import DetailView, ListView

from PodCasts import views
from PodCasts.models import PodCast

urlpatterns = patterns('',
#  url(r'^$', 
#        ListView.as_view(
#            queryset=PodCast.objects.all()[:5],
#            context_object_name='new_podcast_list',
#            template_name='PodCasts/PodCastList.html'),
#        name='index'),
  url(r'^$',             views.PodCastList,    name='index'),
  url(r'^(?P<pk>\d+)/$', views.PodCastDetails, name='detail'),
  url(r'^create/$',      views.create,         name='create'),
  url(r'^favorite/$',    views.UserFavorites,  name='favorites'),
)
