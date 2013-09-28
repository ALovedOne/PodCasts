from PodCasts.models import PodCast,Favorite,Show,Instance

from django.contrib.auth.models import User
from django.conf.urls import patterns, include, url

from rest_framework import viewsets, serializers,routers
from rest_framework.decorators import action, link
from rest_framework.reverse import reverse

class PodCastSerializer(serializers.ModelSerializer):
  '''
    Serializer for podcasts, adds user favorites as a field, if the user is not 
    logged in the field will be false (null or "")
  '''
  userFavorite = serializers.BooleanField(source = 'userFavorited', read_only = True)
  podcastShows = serializers.SerializerMethodField('getShowsURL')

  class Meta:
    model = PodCast
    exclude = ('FavoritingUsers',)

  def getShowsURL(self, podCast):
    return reverse('show-list', request = self.context['request']) + "?podcast=" + str(podCast.id)

class ShowSerializer(serializers.ModelSerializer):
  '''
    Serializer for shows, adds userDone and userPosition fields if a user is 
    logged in, if not then the will be false or 0 respectively
  '''
  userDone = serializers.BooleanField(source = 'userDone', read_only = True)
  userPosition = serializers.IntegerField(source = 'userPosition', read_only = True)
  updateURL = serializers.SerializerMethodField('getUpdateURL')

  class Meta:
    model = Show

  def getUpdateURL(self, obj):
    return reverse('show-detail', request = self.context['request'], kwargs = {'pk':obj.id})
    return "HI"

class PodCastViewSet(viewsets.ModelViewSet):
  model = PodCast
  serializer_class = PodCastSerializer

  def get_queryset(self, *args):
    if self.request.user.is_authenticated():
      qs = PodCast.objects.all(self.request.user.id)
    else:
      qs = PodCast.objects.all()

    if 'favorites' in self.request.QUERY_PARAMS and self.request.user.is_authenticated():
      qs = qs.filter(FavoritingUsers__id = self.request.user.id)

    return qs
 
class ShowViewSet(viewsets.ModelViewSet):
  model = Show
  serializer_class = ShowSerializer

  def get_queryset(self, *args):
    if self.request.user.is_authenticated():
      qs = Show.objects.all(self.request.user.id)
    else:
      qs = Show.objects.all()

    if 'podcast' in self.request.QUERY_PARAMS:
      qs = qs.filter(Podcast_id = self.request.QUERY_PARAMS['podcast'])

    return qs

router = routers.DefaultRouter()
router.register(r'podcasts',  PodCastViewSet, base_name = 'podcasts')
router.register(r'shows',     ShowViewSet)
urlpatterns = router.urls
