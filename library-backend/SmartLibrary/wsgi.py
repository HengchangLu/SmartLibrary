"""
WSGI config for SmartLibrary project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# sys.path.append('/usr/SmartLibrary/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartLibrary.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = 'SmartLibrary.settings'

application = get_wsgi_application()
