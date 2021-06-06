from django.test import SimpleTestCase
from django.urls import reverse, resolve
from text_play.views import index,keyfinder,apple_info,appsearcher,keyword_finder_ajax,getinfo

class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url=reverse('index')
        self.assertEquals(resolve(url).func,index)

    def test_appsearcher_url_is_resolved(self):
        url=reverse('appsearcher')
        self.assertEquals(resolve(url).func,appsearcher)

    def test_keyfinder_url_is_resolved(self):
        url=reverse('keyfinder')
        self.assertEquals(resolve(url).func,keyfinder)

    def test_getinfo_url_is_resolved(self):
        url=reverse('getinfo')
        self.assertEquals(resolve(url).func,getinfo)

    def test_apple_info_url_is_resolved(self):
        url=reverse('apple_info')
        self.assertEquals(resolve(url).func,apple_info)

    def test_keyword_finder_ajax_url_is_resolved(self):
        url=reverse('keyword_finder_ajax')
        self.assertEquals(resolve(url).func,keyword_finder_ajax)
