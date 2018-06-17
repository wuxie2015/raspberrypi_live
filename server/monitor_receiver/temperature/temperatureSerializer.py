# -*- coding: utf-8 -*-
import operator
from rest_framework import serializers
from temperature.models import TemperatureRecorde


class temperatureSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    createTime = serializers.DateTimeField(read_only=True)
    
    def validate_temperature(self,temperature):
        try:
            float(temperature)
        except (ValueError,TypeError):
            raise  serializers.ValidationError("temperature %s illegal, it must be float"%temperature)
        else:
            if float(temperature) > 50.0:
                raise serializers.ValidationError("temperature %s too high"%temperature)
        return temperature
    
    def validate_humidity(self, humidity):
        try:
            float(humidity)
        except (ValueError,TypeError):
            raise  serializers.ValidationError("humidity %s illegal, it must be float"%humidity)
        return humidity
    
    class Meta:
        model = TemperatureRecorde
        fields = (
            'id',
            'temperature',
            'humidity',
            'createTime')