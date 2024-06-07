from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from .forms import SignupForm
from django.contrib.auth.models import User


class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:signin')


class SigninView(LoginView):
    template_name = 'users/signin.html'
    redirect_authenticated_user = True
    #success_url = reverse_lazy('cars')

    def get_success_url(self):
        return reverse_lazy('parking:cars')
