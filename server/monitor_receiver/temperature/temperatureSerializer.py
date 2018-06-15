# -*- coding: utf-8 -*-
import operator
from rest_framework import serializers
from temperature.models import TemperatureRecorde


class temperatureSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    createTime = serializers.DateTimeField(read_only=True)
    class Meta:
        model = TemperatureRecorde
        fields = (
            'id',
            'temperature',
            'createTime')