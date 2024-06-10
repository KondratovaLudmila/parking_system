from django.urls import path
from . import views

app_name = 'parking'

urlpatterns = [
    path('', views.CarsView.as_view(), name='cars'),
    path('car/', views.CarCreateView.as_view(), name='car_add'),
    path('parking_report/', views.parking_report, name='parking_report'),
    path('download_reports/', views.download_reports, name='download_reports'),
]