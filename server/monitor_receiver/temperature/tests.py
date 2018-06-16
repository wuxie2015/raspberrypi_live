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
        self.default_create_data = temperature_obj_1.to_dict()
        self.temperature_id = temperature_obj_1.id

    def test_list(self):
        data_dict = {
            'start_timestamp': '1529027117'
        }
        response = self.client.get('/temperature/templist',
                                   data=data_dict,
                                   content_type='application/json')
        try:
            self.assertEqual(response.status_code, 200)
        except AssertionError as e:
            print('Ops in test_list')
            print(response.data)
            raise AssertionError(e)

    def test_create(self):
        default_create = {
            'temperature': 33
        }
        response = self.client.post(
            '/temperature/templist',
            data=json.dumps(default_create),
            content_type='application/json')
        try:
            self.assertEqual(response.status_code, 201)
            response_content = response.data
            for key in default_create:
                self.assertEqual(
                    type(
                        default_create[key])(
                        response_content[key]),
                    default_create[key])
        except AssertionError as e:
            print('Ops in test_create')
            print(response.data)
            raise AssertionError(e)

    def test_get(self):
        response = self.client.get(
            "/temperature/templist/%s" %self.temperature_id)
        try:
            self.assertEqual(response.status_code, 200)
            #self.assertEqual(len(response.data),1)
            response_content = response.data
            for key in self.default_create_data:
                if not key == 'createTime':
                    self.assertEqual(
                        type(
                            self.default_create_data[key])(
                            response_content[key]),
                        self.default_create_data[key])
        except AssertionError as e:
            print('Ops in test_get')
            print(response.data)
            raise AssertionError(e)

    def test_put(self):
        default_put = {
            'temperature': 32
        }
        response = self.client.put(
            "/temperature/templist/%s" %self.temperature_id,
            data=json.dumps(default_put),
            content_type='application/json')
        try:
            self.assertEqual(response.status_code, 200)
            response_content = response.data
            for key in default_put:
                self.assertEqual(
                    type(
                        default_put[key])(
                        response_content[key]),
                    default_put[key])
        except AssertionError as e:
            print('Ops in test_put')
            print(response.data)
            raise AssertionError(e)

    def test_patch(self):
        default_put = {
            'temperature': 32
        }
        response = self.client.patch(
            "/temperature/templist/%s" %self.temperature_id,
            data=json.dumps(default_put),
            content_type='application/json')
        try:
            self.assertEqual(response.status_code, 200)
            response_content = response.data
            for key in default_put:
                self.assertEqual(
                    type(
                        default_put[key])(
                        response_content[key]),
                    default_put[key])
        except AssertionError as e:
            print('Ops in test_patch')
            print(response.data)
            raise AssertionError(e)

    def test_delete(self):
        response = self.client.delete(
            "/temperature/templist/%s"%self.temperature_id)
        self.assertEqual(response.status_code, 204)
