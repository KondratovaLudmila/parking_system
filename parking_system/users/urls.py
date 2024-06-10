from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('signin/', views.SigninView.as_view(), name='signin'),
    path('signout/', views.LogoutView.as_view(next_page='users:signin'), name='signout'),
    path('profile/', views.UserUpdateView.as_view(), name='profile'),
]