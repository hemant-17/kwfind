from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('appsearcher/',views.appsearcher,name='appsearcher'),
    path('keywordfind/',views.keyfinder,name='keyfinder'),
    path('getinfo',views.getinfo, name="getinfo"),
    path('apple_info',views.apple_info, name="apple_info"),
    path('keyword_finder_ajax',views.keyword_finder_ajax, name="keyword_finder_ajax"),

]