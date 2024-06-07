from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


from .models import Car

@method_decorator(login_required, name='dispatch')
class CarsView(TemplateView):
    template_name = 'parking/index.html'


    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        
        if self.request.user.is_superuser:
            context['cars'] = Car.objects.all()
        else:
            context['cars'] = Car.objects.filter(user=self.request.user)
        return context
    

@method_decorator(login_required, name='dispatch')
class CarCreateView(CreateView):
    model = Car
    fields = ['reg_mark', 'model', 'color', 'fare', 'user']
    success_url = reverse_lazy("parking:cars")




