import os
import django
import logging


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartLibrary-settings")
django.setup()
logger = logging.getLogger('django')
