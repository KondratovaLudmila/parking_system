from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required, user_passes_test
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

@login_required
def parking_report(request):
    if request.user.is_superuser:
        cars = Car.objects.all()
    else:
        cars = Car.objects.filter(user=request.user)

    reports = []
    for car in cars:
        total_duration = car.total_parking_duration()
        total_cost = car.total_parking_cost()
        reports.append({
            'registration_mark': car.reg_mark,
            'total_duration': total_duration,
            'total_cost': total_cost,
            'user': car.user
        })

    return render(request, 'parking/report.html', {'reports': reports})

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def download_reports(request):
    cars = Car.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="all_parking_reports.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Registration Mark', 'Total Duration (seconds)', 'Total Cost', 'User'])

    for car in cars:
        total_duration = car.total_parking_duration()
        total_cost = car.total_parking_cost()
        writer.writerow([car.reg_mark, total_duration, total_cost, car.user.username])

    return response
