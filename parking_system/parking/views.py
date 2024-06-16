from typing import Any

from django.db.models import Q
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect

from datetime import datetime, timezone

import csv

from users.models import Profile
from .models import Car, Park, ParkingInfo, Ban
from .decorators import superuser_required
from .forms import CarForm
from numberplate_ukr.main import CarPlateReader


@method_decorator(login_required, name='dispatch')
class CarsView(TemplateView):
    template_name = 'parking/index.html'

    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)

        query = self.request.GET.get('q')

        if query:
            if self.request.user.is_superuser:
                cars = Car.objects.filter(
                    (Q(reg_mark__startswith=query) |
                    Q(color__startswith=query) |
                    Q(model__startswith=query)) &
                    Q(is_banned=False)
                ).order_by('confirmed')
            else:
                cars = Car.objects.filter(
                    Q(user=self.request.user) &
                    (Q(reg_mark__startswith=query) |
                     Q(color__startswith=query) |
                     Q(model__startswith=query)) & Q(is_banned=False)
                ).order_by('confirmed')
        else:
            if self.request.user.is_superuser:
                cars = Car.objects.filter(is_banned=False).order_by('confirmed')
            else:
                cars = Car.objects.filter(user=self.request.user)

        context['cars'] = cars
        return context
    

@method_decorator(login_required, name='dispatch')
class CarCreateView(CreateView):
    model = Car
    fields = ['reg_mark', 'model', 'color', 'fare', 'user', 'confirmed']
    success_url = reverse_lazy("parking:cars")

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['parking_info'] = ParkingInfo.objects.first()
        return context
    

@method_decorator(login_required, name='dispatch')
class CarsBanList(ListView):
    model = Car
    template_name = 'parking/ban_list.html'
    context_object_name = 'banned_cars'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            if self.request.user.is_superuser:
                cars = Car.objects.filter(
                    (Q(reg_mark__startswith=query) |
                    Q(color__startswith=query) |
                    Q(model__startswith=query)) &
                    Q(is_banned=True)
                ).order_by('confirmed')
            else:
                cars = Car.objects.filter(
                    Q(user=self.request.user) &
                    (Q(reg_mark__startswith=query) |
                     Q(color__startswith=query) |
                     Q(model__startswith=query)) & Q(is_banned=True)
                ).order_by('confirmed')
        else:
            if self.request.user.is_superuser:
                cars = Car.objects.filter(is_banned=True).order_by('confirmed')
            else:
                cars = Car.objects.filter(user=self.request.user)

        cars = cars.prefetch_related('ban_set')
        return cars



@method_decorator(login_required, name='dispatch')
class DebtorListView(ListView):
    model = Profile
    template_name = 'parking/debtor_list.html'
    context_object_name = 'debtors'

    def get_queryset(self):
        return self.model.objects.filter(balance__lt=0)
    

# class DownloadCSVView(View):
#     model = Payment
#     fields = ['']

#     def get(self, request, *args, **kwargs):
#         debtors = 
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="debtor_report.csv"'

#         if blob_content:
#             response = HttpResponse(blob_content.readall(), content_type=file_type)
#             response['Content-Disposition'] = f'attachment; filename={filename}'
#             messages.success(request, f"{filename} was successfully downloaded")
#             return response

#         return Http404


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
class ParkingGreetView(DetailView):
    template_name = "parking/parking_greet.html"
    model = Park

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['duration'] = context['object'].duration_to_str()
        context['payment'] = self.request.user.profile
        
        return context


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
        car = None
        text = []
        message = f"Your car number {''.join(text)} was not detected or not register. Plase contact the administrator!"
        for file_name in request.FILES:
            file = bytearray(request.FILES[file_name].read())
            text = CarPlateReader().img_process(file)
            car = Car.objects.filter(user=request.user, reg_mark__in=text).first()

            if car is not None:
                break
        
        if car is not None and car.confirmed and not car.is_banned:
            park = Park.objects.filter(car=car, out_time=None).first()

            if park:
                park.out_time = datetime.now(timezone.utc)
                park.save()
                
            else:
                park = Park(car=car)
                park.save()
            
            return redirect('parking:parking_greet', park.pk)

        else:
            if text:
                message = f"Your car number {''.join(text)} not register. Plase contact the administrator!"
            else:
                message = f"Your car number was not detected. Plase try again!" 
            return render(request, 'parking/parking.html', {'message': message, 'car': car})
        

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


@csrf_protect
def delete_car(request, id):
    if request.method == 'POST':
        item = get_object_or_404(Car, id=id)
        item.delete()
        return redirect('parking:cars')
    return HttpResponse(status=405)


@csrf_protect
def edit_car(request, id):
    item = get_object_or_404(Car, id=id)
    if request.method == 'POST':
        form = CarForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('parking:cars')
    else:
        form = CarForm(instance=item)
    return render(request, 'parking/edit_car.html', {'form': form, 'car': item})


@login_required
@csrf_protect
def ban_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reason = request.POST.get('reason', '')
    if request.method == 'POST':
        Ban.objects.create(car=car, reason=reason)
        car.is_banned = True
        car.save()
        return redirect('parking:cars')
    return HttpResponse(status=405)


@login_required
@csrf_protect
def unban_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        ban = get_object_or_404(Ban, car=car)
        ban.delete()
        car.is_banned = False
        car.save()
        return redirect('parking:ban_list')
    return HttpResponse(status=405)
