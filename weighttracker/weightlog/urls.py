from urllib.parse import urlparse
from django.urls import path
from weightlog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('weights/', views.WeightListView.as_view(), name='weights'),
    path('weight/<int:pk>', views.WeightDetailView.as_view(), name='weight-detail'),
]

# urls for weight forms
urlpatterns += [
    path('weight/create/', views.WeightCreate.as_view(), name='weight-create'),
    path('weight/<int:pk>/update/', views.WeightUpdate.as_view(), name='weight-update'),
    path('weight/<int:pk>/delete/', views.WeightDelete.as_view(), name='weight-delete'),
]

# urls for charts
urlpatterns += [
    # shows the actual chart
    path('chart/<int:pk>', views.lineChart.as_view(), name='chart'),
    # returns JSON data for the chart -> pk = days back
    path('api/chart/data/<int:pk>', views.chart_data, name='api-data'),
]