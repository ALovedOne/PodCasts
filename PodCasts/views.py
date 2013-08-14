from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader

from PodCasts.models import PodCast, Show, Favorite

# Create your views here.
def create(request):
    p = None
    podcast_url = request.POST['podcast_url']
    podcast_url = podcast_url.lower().strip()
    (p, created) = PodCast.objects.get_or_create(Link=podcast_url)
    if created:
        p.update(True)
    else:
      p.updateIfReq()

    return HttpResponseRedirect(reverse('detail', args=(p.id,)))

def PodCastList(request):
    podCasts = PodCast.objects.all()
    if request.user.is_authenticated():
        for i in podCasts:
            i.currentUser = request.user
    context = {'new_podcast_list': podCasts,
               'user': request.user }
    return render(request, 'PodCasts/PodCastList.html', context)

def PodCastDetails(request, pk):
    podcast = get_object_or_404(PodCast, pk=pk)
    podcast.updateIfReq()
    shows = Show.objects.filter(Podcast = podcast).order_by('-PubDate')
    context = { 'podcast' : podcast,
                'shows' : shows,
                'user': request.user }
    return render(request, 'PodCasts/PodCast.html', context)
 
@login_required
def UserFavorites(request):
    if not request.user.is_authenticated():
        return redirect_to_login(PodCasts.view.UserFavorites)
    user_favorites = Favorite.objects.filter(User = request.user.id)
    context = { 'favorites' : user_favorites,
                'user': request.user }
    return render(request, 'PodCasts/Favorites.html', context)
