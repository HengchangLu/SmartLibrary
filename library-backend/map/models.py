from django.db import models
from datetime import datetime


class UserLocation(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户行走位置信息"
        verbose_name_plural = verbose_name
