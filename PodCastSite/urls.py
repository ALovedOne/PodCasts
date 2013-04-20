from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'podcast.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^PodCasts/', include('PodCasts.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

