from django.contrib import admin
from django.urls import re_path, include
#Custom claims in token
from .views import *


urlpatterns = [
    re_path(r'^getrandom/', get_random_news_items, name='getrandom'),
]

