from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from text_play.models import Keyword,Url,Mapping_of_url
import json

class TestViews(TestCase):
    def setUp(self):
        self.client=Client()

    def test_apple_info(self):
        response=self.client.post(
            self.apple_info,{
                'appname':'',
                'appid':1367822033
            })
        self.assertEquals(response.status_code,302)
