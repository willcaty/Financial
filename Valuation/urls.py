# -*- coding: utf-8 -*-

from django.urls import path
from .views import *

urlpatterns = [
    path('index/', index, name='index'),
    path('a/', scrapy_view),
]