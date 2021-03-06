from urllib.parse import urlparse
from django.urls import path
from weightlog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit/profile/<int:pk>', views.UserProfileUpdate.as_view(), name='edit-profile'),
]

# urls for weight forms
urlpatterns += [
    path('weight/create/', views.WeightCreate.as_view(), name='weight-create'),
    path('weight/<int:pk>/update/', views.WeightUpdate.as_view(), name='weight-update'),
]

# urls for charts
urlpatterns += [
    # shows the actual chart
    path('chart/<int:pk>', views.lineChart.as_view(), name='chart'),
    # returns JSON data for the chart -> pk = days back
    path('api/chart/data/<int:pk>', views.chart_data, name='api-data'),
]