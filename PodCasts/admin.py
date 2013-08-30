from django.contrib import admin
from PodCasts.models import PodCast, Favorite

# Register your models here.
admin.site.register(PodCast)
admin.site.register(Favorite)
