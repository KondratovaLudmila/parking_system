from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Car, Park
import csv

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


def parking_report(request):
    cars = Car.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="parking_report.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Registration Mark', 'Total Duration (seconds)', 'Total Cost'])

    for car in cars:
        total_duration = car.total_parking_duration()
        total_cost = car.total_parking_cost()
        writer.writerow([car.reg_mark, total_duration, total_cost])

    return response




