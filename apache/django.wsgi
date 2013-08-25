import os,sys

path = '/home/mike/PodCasts/'
if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'PodCastSite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()



