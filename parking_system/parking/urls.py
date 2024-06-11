from django.urls import path
from . import views

app_name = 'parking'

urlpatterns = [
    path('', views.CarsView.as_view(), name='cars'),
    path('car/', views.CarCreateView.as_view(), name='car_add'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('parking/', views.parking, name='parking'),
    path('parking_info/', views.SettingsView.as_view(), name='parking_info'),
    path('parking/in/', views.ParkingInView.as_view(), name='parking_in'),
    path('parking/out/', views.ParkingOutView.as_view(), name='parking_out'),
    path('parking_report/', views.parking_report, name='parking_report'),
    path('download_reports/', views.download_reports, name='download_reports'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
    path('edit/<int:id>/', views.edit_car, name='edit_car'),
    path('ban/<int:car_id>/', views.ban_car, name='ban_car'),
    path('unban/<int:car_id>/', views.unban_car, name='unban_car'),
]