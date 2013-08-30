from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *

from PodCasts.support.Parsers import RSSParser

import datetime
import pytz

class PodCastManager(models.Manager):
    def all(self, userID = None):
      if userID:
          return super(PodCastManager, self).all().extra(
            select = {'userFavorited': '''
              EXISTS (
                SELECT * 
                FROM PodCasts_favorite
                WHERE PodCasts_favorite.User_id = %s AND
                      PodCasts_favorite.Podcast_id = PodCasts_podcast.id)'''},
            select_params = (userID,))
      else:
          return super(PodCastManager, self).all()
      

# Create your models here.
class PodCast(models.Model):
    Title = models.CharField(max_length=200)
    Link  = models.URLField(unique=True)
    ImageLink = models.URLField(blank=True, default="")
    Description = models.TextField()
    LastRetrived = models.DateTimeField(blank=True,null=True)
    FavoritingUsers = models.ManyToManyField(User, through = 'Favorite')

    objects = PodCastManager()

    _favorited = False

    @property
    def userFavorited(self):
      return not not self._favorited

    @userFavorited.setter
    def userFavorited(self, value):
      self._favorited = value

    def __unicode__(self):
        return self.Title

    def timeSinceLastUpdate(self):
        now = datetime.datetime.now(pytz.utc)
        dateDelta = now - self.LastRetrived
        return dateDelta.seconds + dateDelta.days*60*60*24

    def updateIfReq(self):
        if self.timeSinceLastUpdate() > 60*60:
            self.update()

    def update(self, FirstLoad = True):
        parser = RSSParser(self.Link)

        self.Title = parser.Title
        self.LastRetrived = datetime.datetime.now(pytz.utc)
        self.Description = parser.Description
        self.ImageLink = parser.ImageLink
        self.save()

        for i in parser.Items:
            if i.MediaSize == "":
                MediaSize = 0
            else:
                MediaSize = i.MediaSize
            if i.MediaURL != "":
                (show, created) = Show.objects.get_or_create(Podcast = self, GUID = i.GUID)
                if created:
                    show.Title = i.Title
                    show.Description = i.Description
                    show.Link = i.Link
                    show.MediaSize = MediaSize
                    show.MediaType = i.MediaType
                    show.MediaURL = i.MediaURL
                    show.PubDate = i.PubDate
                    show.save()
        self.LastRetrived = datetime.datetime.now(pytz.utc)
        self.save()

class ShowManager(models.Manager):
    def all(self, userID = None):
      if userID:
          return self.raw('''
SELECT  PodCasts_show.*, 
        UserInst.Position as userPosition, 
        UserInst.Done as userDone
FROM PodCasts_show
LEFT JOIN (
  SELECT *
  FROM PodCasts_instance
  WHERE PodCasts_instance.User_id = %s
) AS UserInsts
ON PodCasts_show.id = UserInsts.Show_id''', userID)
      else:
          return super(ShowManager, self).all()
      
class Show(models.Model):
    Podcast = models.ForeignKey(PodCast,related_name = 'shows')
    Title = models.CharField(max_length=200)
    GUID  = models.CharField(max_length=200,unique=True)
    Link  = models.CharField(max_length=200)
    MediaSize = models.IntegerField(default=0)
    MediaURL  = models.URLField()
    MediaType = models.CharField(max_length=32)
    Description = models.TextField()
    PubDate = models.DateField(null=True)

    objects = ShowManager()

    _userPosition = -1
    _userDone = False

    @property
    def userPosition(self):
      return self._userPosition

    @userPosition.setter
    def userPosition(self, value):
      self._userPosition = value

    @property
    def userDone(self):
      return not not self._userDone

    @userDone.setter
    def userDone(self, value):
      self._userDone = value

    def __unicode__(self):
        return self.Title + " [" + str(self.id) + "]"

class Favorite(models.Model):
    User = models.ForeignKey(User,related_name='favorites')
    Podcast = models.ForeignKey(PodCast)
    
class Instance(models.Model):
    User = models.ForeignKey(User)
    Show = models.ForeignKey(Show)
    PodCast = models.ForeignKey(PodCast)
    Position = models.IntegerField(default=0)
    Done = models.BooleanField(default=False)
