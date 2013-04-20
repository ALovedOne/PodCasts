from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import *

from PodCasts.support.Parsers import RSSParser

import datetime
import pytz

# Create your models here.
class PodCast(models.Model):
    Title = models.CharField(max_length=200)
    Link  = models.URLField(unique=True)
    Description = models.TextField()
    LastRetrived = models.DateTimeField(blank=True,null=True)
    
    _isFavorite = False
    _user = None

    @property
    def isFavorite(self):
        if self._user:
            return Favorite.objects.filter(User = self._user, Podcast = self)
        else:
            return False

    @isFavorite.setter
    def isFavorite(self, value):
        self._isFavorite = value
    
    @property
    def currentUser(self):
        return self._user
    
    @currentUser.setter
    def currentUser(self, user):
        self._user = user

    def __unicode__(self):
        return self.Title

    def timeSinceLastUpdate(self):
        now = datetime.datetime.now(pytz.utc)
        dateDelta = now - self.LastRetrived
        return dateDelta.seconds + dateDelta.days*60*60*24

    def updateIfReq(self):
        if self.timeSinceLastUpdate() > 60*60:
            self.update()

    def update(self, FirstLoad = False):
        print self.Link
        parser = RSSParser(self.Link)

        if FirstLoad:
            self.Title = parser.Title
            self.LastRetrived = datetime.datetime.now(pytz.utc)
            self.Description = parser.Description
            self.save()

        for i in parser.Items:
            print i.Title
            print "  " + i.MediaURL
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

class Show(models.Model):
    Podcast = models.ForeignKey(PodCast)
    Title = models.CharField(max_length=200)
    GUID  = models.CharField(max_length=200,unique=True)
    Link  = models.CharField(max_length=200)
    MediaSize = models.IntegerField(default=0)
    MediaURL  = models.URLField()
    MediaType = models.CharField(max_length=32)
    Description = models.TextField()
    PubDate = models.DateField(null=True)

    def __unicode__(self):
        return self.Title

class Favorite(models.Model):
    User = models.ForeignKey(User)
    Podcast = models.ForeignKey(PodCast)
    
class Instance(models.Model):
    User = models.ForeignKey(User)
    Show = models.ForeignKey(Show)
    Position = models.IntegerField(default=0)
    Done = models.BooleanField(default=False)
