# from django.http import response
# from django.test import TestCase, Client
# from django.urls import reverse
# from text_play.models import Keyword,Url,Mapping_of_url
# import json

# class TestViews(TestCase):
#     def setUp(self):
#         self.client=Client()

#     def test_apple_info(self):
#         resp = self.client.get(reverse("getinfo"))
#         response=self.client.post(
#             resp,{
#                 'appname':'',
#                 'appid':''
#             })
#         self.assertEquals(response.status_code,404
#         )

#     def test_get_info(self):
#         resp = self.client.get(reverse("getinfo"))
#         response=self.client.post(
#             resp,{
#                 'packagename':'com.appxplore.voidtroopers'
#             })
#         self.assertEquals(response.status_code,200)
