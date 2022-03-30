from urllib.parse import urlparse
from django.urls import path
from weightlog import views

urlpatterns = [
    path('', views.index, name='index'),
]