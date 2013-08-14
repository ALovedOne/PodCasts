from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

from django.contrib.auth import views,forms


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'podcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/',        include(admin.site.urls)),
    url(r'^PodCasts/',     include('PodCasts.urls')),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^api/',             include('PodCastSite.api.urls')), 
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/',views.logout,name='logout'),
)

