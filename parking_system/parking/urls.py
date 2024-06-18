from django.urls import path
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from . import views

app_name = 'parking'

urlpatterns = [
    path('', views.CarsView.as_view(), name='cars'),
    path('car/', views.CarCreateView.as_view(), name='car_add'),
    path('history/', views.HistoryView.as_view(), name='history'),
    path('parking/', views.parking, name='parking'),
    path('parking_info/', views.SettingsView.as_view(), name='parking_info'),
    path('parking/<pk>/', views.ParkingGreetView.as_view(), name='parking_greet'),
    path('parking_report/', views.parking_report, name='parking_report'),
    path('download_reports/', views.download_reports, name='download_reports'),
    path('delete/<int:id>/', views.delete_car, name='delete_car'),
    path('edit/<int:id>/', views.edit_car, name='edit_car'),
    path('ban/<int:car_id>/', views.ban_car, name='ban_car'),
    path('unban/<int:car_id>/', views.unban_car, name='unban_car'),
    path('search/', views.CarsView.as_view(), name='search_cars'),
    path('searchbanlist/', views.CarsBanList.as_view(), name='search_banned_cars'),
    path('ban_list/', views.CarsBanList.as_view(), name='ban_list'),
    path('debtor_report/', views.DebtorListView.as_view(), name='debtor_report'),
    path('payment/', views.PaymentListView.as_view(), name="payment"),
    path('payment/pay/<int:amount>/', views.PayView.as_view(), name='pay'),
    path('payment/pay_callback/', views.PayCallbackView.as_view(), name='pay_callback'),
    #path('debtor_report/download', views.DebtorListView.as_view(), name='download_debtors'),
]