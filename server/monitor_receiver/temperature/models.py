# -*- coding: utf-8 -*-
import mongoengine

from django.db import models
import uuid

# Create your models here.

class temperatureRecorde(mongoengine.Document):
    id = mongoengine.UUIDField('uuid',primary_key=True, default=uuid.uuid4)
    temperature = models.IntegerField('当前温度',null=True, default=0)
    createTime = models.DateTimeField('数据创建时间',
                                      auto_now_add=True, db_index=True, null=True)

    class Meta:
        db_table = 'temperature_recorde'
        ordering = ['-createTime']