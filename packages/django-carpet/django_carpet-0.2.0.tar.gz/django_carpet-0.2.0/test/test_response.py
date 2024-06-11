# Django
from django.test import TestCase

from django_carpet.response import VieoloResponse


class ResponseTest(TestCase):

    def test_vieolo_response(self):
        vr = VieoloResponse('success', 'items')
        vr.response_object['items'] = [{"id": 1, "name": "one"}, {"id": 2, "name": "two"}, {"id": 3, "name": "three"}]
        
        self.assertEqual(len(vr.data), 3)

        filterd_data = vr.filter(lambda x: x["id"] < 3) 
        self.assertEqual(len(filterd_data), 2)
        self.assertEqual(filterd_data[0]["id"], 1)
        self.assertEqual(filterd_data[1]["id"], 2)