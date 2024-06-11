from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import datetime, timezone

from .models import Car, Park, ParkingInfo
from .decorators import superuser_required
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

        
@method_decorator(login_required, name='dispatch')
class HistoryView(TemplateView):
    template_name = "parking/history.html"

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        
        context['history'] = Park.objects.filter(car__user=self.request.user).order_by('-in_time').values('car__reg_mark', 
                                                                                                          'in_time', 
                                                                                                          'out_time', 
                                                                                                          'cost',
                                                                                                          'out_time')
        return context


@method_decorator(login_required, name='dispatch')
class ParkingInView(TemplateView):
    template_name = "parking/parking_wellcome.html"


@method_decorator(login_required, name='dispatch')
class ParkingOutView(TemplateView):
    template_name = "parking/parking_goodbye.html"


@method_decorator(superuser_required, name='dispatch')
class SettingsView(UpdateView):
    model = ParkingInfo
    fields = ['address', 'places', 'limit', 'default_fare']
    success_url = reverse_lazy('parking:parking_info')

    def get_object(self, queryset=None) -> Model:
        first = ParkingInfo.objects.first()
        # We need to be shure that we hawe a record
        if first is None:
            object = ParkingInfo.objects.create()
        else:
            object = ParkingInfo.objects.get(id=first.id)
        return object


@login_required
def parking(request):
    if request.method == 'POST':
        message = "Your car number was not detected or not register. Plase contact the administrator!"
        reg_mark = None
        for file_name in request.FILES:
            car = Car.objects.filter(user=request.user).first()
            if car is not None:
                reg_mark = car.reg_mark
            break

        success = reg_mark is not None
        
        if success:
            car = Car.objects.filter(reg_mark=reg_mark, user=request.user).first()
            success = car is not None
        
        if success:
            park = Park.objects.filter(car=car, out_time=None).first()

            if park:
                park.out_time = datetime.now(timezone.utc)
                park.save()
                return redirect(to='parking:parking_out')
            else:
                park = Park(car=car)
                park.save()
                return redirect(to='parking:parking_in')

        else:
            return render(request, 'parking/parking.html', {'message': message})
        

    return render(request, 'parking/parking.html')


@login_required
def parking_report(request):
    if request.user.is_superuser:
        cars = Car.objects.all()
    else:
        cars = Car.objects.filter(user=request.user)

    reports = []
    for car in cars:
        total_duration = car.total_parking_duration()
        hours, remainder = divmod(total_duration, 3600)
        minutes, seconds = divmod(remainder, 60)
        total_duration_str = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        total_cost = car.total_parking_cost()
        reports.append({
            'registration_mark': car.reg_mark,
            'total_duration': total_duration_str,
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
