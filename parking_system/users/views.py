from typing import Any
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


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

    def get_success_url(self):
        return reverse_lazy('parking:cars')
    

@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/profile.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('users:profile')


    def get(self, request, **kwargs):
        self.object = User.objects.get(username=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)
    
    
    def get_object(self, queryset=None):
        return self.request.user
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    html_email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'users/password_reset_subject.txt'




