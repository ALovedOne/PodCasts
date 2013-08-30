from PodCasts.models import PodCast,Favorite,Show,Instance

from django.contrib.auth.models import User

from rest_framework import viewsets, serializers

class PodCastSerializer(serializers.ModelSerializer):
  '''
    Serializer for podcasts, adds user favorites as a field, if the user is not 
    logged in the field will be false (null or "")
  '''
  userFavorite = serializers.BooleanField(source = 'userFavorited', read_only = True)

  class Meta:
    model = PodCast
    exclude = ('FavoritingUsers',)

class ShowSerializer(serializers.ModelSerializer):
  '''
    Serializer for shows, adds userDone and userPosition fields if a user is 
    logged in, if not then the will be false or 0 respectively
  '''
  userDone = serializers.BooleanField(source = 'userDone', read_only = True)
  userPosition = serializers.IntegerField(source = 'userPosition', read_only = True)

  class Meta:
    model = Show

class PodCastViewSet(viewsets.ModelViewSet):
  model = PodCast
  serializer_class = PodCastSerializer

  def get_queryset(self, *args):
    if self.request.user.is_authenticated():
      return PodCast.objects.all(self.request.user.id)
    else:
      return PodCast.objects.all()

class ShowViewSet(viewsets.ModelViewSet):
  model = Show
  serializer_class = ShowSerializer

  def get_queryset(self, *args):
    print dir(self)
    if self.request.user.is_authenticated():
      return Show.objects.all(self.request.user.id)
    else:
      return Show.objects.all()

class FavoriteViewSet(viewsets.ModelViewSet):
  model = PodCast
  serializer_class = PodCastSerializer

  def get_queryset(self):
    return PodCast.objects.filter(FavoritingUsers__id = self.request.user.id)

