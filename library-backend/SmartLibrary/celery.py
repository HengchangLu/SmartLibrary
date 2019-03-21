from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from SmartLibrary import settings
# from django.conf import settings
"""
celery 4.0+
"""

# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SmartLibrary.settings')

# 注册celery的APP
app = Celery('SmartLibrary')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# 绑定配置文件
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# 自动发现每个app下的tasks.py文件


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
