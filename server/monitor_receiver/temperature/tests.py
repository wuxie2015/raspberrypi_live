# -*- coding: utf-8 -*-
from django.test import TestCase
import json
from temperature.models import TemperatureRecorde

# Create your tests here.

class TemperatureTest(TestCase):
    def setUp(self):
        temperature_obj_1 = TemperatureRecorde.objects.create(
            temperature = 32
        )
        temperature_obj_1.save()
        self.temperature_id = temperature_obj_1.id

    def test_list(self):
        data_dict = {
            'start_timestamp': '1529027117'
        }
        response = self.client.get('/host/baseinfo',
                                   data=data_dict,
                                   content_type='application/json')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            print('Ops in test_list')
            print(response.data)
            raise AssertionError(e)