# -*- coding: utf-8 -*-
import logging
import traceback
from django.http import Http404
from temperature.models import TemperatureRecorde
from temperature.temperatureSerializer import temperatureSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import mixins
import time

logger = logging.getLogger(__name__)

# Create your views here.
class temperatureList(generics.ListCreateAPIView,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin
                  ):

    queryset = TemperatureRecorde.objects.all()
    serializer_class = temperatureSerializer

    def get(self, request, *args, **kwargs):
        try:
            start_time_list = request.data.get('start_timestamp',None)
            if start_time_list:
                timeArray = time.localtime(start_time_list)
                time_obj = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                self.queryset = TemperatureRecorde.objects.filter(createTime__gt = time_obj)
            else:
                self.queryset = TemperatureRecorde.objects.all()
            return self.list(request, *args, **kwargs)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            result = self.create(request, *args, **kwargs)
            return result
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class temperatureDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemperatureRecorde.objects.all()
    serializer_class = temperatureSerializer

    def get_object(self,**kwargs):
        try:
            temperature_id = kwargs['temperature_id']
            result = TemperatureRecorde.objects.filter(id=temperature_id).first()
            return result
        except BaseException:
            logger.error(traceback.format_exc())
            raise Http404

    def get(self, request, *args, **kwargs):
        try:
            temperature_id = kwargs['temperature_id']
            temps = self.get_object(temperature_id=temperature_id)
            temp_serialized = temperatureSerializer(temps)
            return Response(temp_serialized.data)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, *args, **kwargs):
        try:
            temperature_id = kwargs['temperature_id']
            temps = self.get_object(temperature_id=temperature_id)
            try:
                serializer = temperatureSerializer(instance=temps,data=request.data)
            except ValueError as e:
                logger.error(traceback.format_exc())
                return Response(
                    e.args, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            temperature_id = kwargs['temperature_id']
            temps = self.get_object(temperature_id=temperature_id)
            try:
                serializer = self.get_serializer(instance=temps, data=request.data, partial=True)
            except ValueError as e:
                logger.error(traceback.format_exc())
                return Response(
                    e.args, status=status.HTTP_400_BAD_REQUEST)
            if serializer.is_valid():
                self.perform_update(serializer)
                return Response(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_400_BAD_REQUEST)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            temperature_id = kwargs['temperature_id']
            temps = self.get_object(temperature_id=temperature_id)
            self.perform_destroy(temps)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except BaseException as e:
            logger.error(traceback.format_exc())
            return Response(
                e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
