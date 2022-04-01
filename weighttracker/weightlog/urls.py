from urllib.parse import urlparse
from django.urls import path
from weightlog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weight/', views.WeightListView.as_view(), name='weight-list'),
    path('weight/<int:pk>', views.WeightDetailView.as_view(), name='weight-detail'),
]