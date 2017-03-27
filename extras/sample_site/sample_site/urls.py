import os

from django.conf import settings
from django.conf.urls import include, url

from app import views

urlpatterns = [
    url(r'^$', views.page),
]
