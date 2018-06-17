# -*- coding: utf-8 -*-
from django.db import models
import uuid

# Create your models here.

class TemperatureRecorde(models.Model):
    id = models.UUIDField('uuid',primary_key=True, default=uuid.uuid4)
    temperature = models.FloatField('当前温度',null=True, default=0)
    humidity = models.FloatField('当前湿度',null=True, default=0)
    createTime = models.DateTimeField('数据创建时间',
                                      auto_now_add=True, db_index=True, null=True)

    class Meta:
        db_table = 'temperature_recorde'
        ordering = ['-createTime']

    def to_dict(self):
        return dict(
            id = self.id,
            temperature = self.temperature,
            createTime = self.createTime,
        )
