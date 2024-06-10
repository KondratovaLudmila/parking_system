from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    reg_mark = models.CharField(max_length=8, null=False, unique=True)
    model = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=30, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    fare = models.FloatField(default=0)
    confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.reg_mark}"

    def total_parking_duration(self):
        total_duration = 0
        parks = self.park_set.all()
        for park in parks:
            if park.out_time:
                duration = (park.out_time - park.in_time).total_seconds()
                total_duration += duration
        return total_duration

    def total_parking_cost(self):
        total_cost = 0
        parks = self.park_set.all()
        for park in parks:
            total_cost += park.cost
        return total_cost


class Park(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(null=True, blank=True)
    cost = models.FloatField(default=0)


    def calculate_cost(self):
        if self.out_time:
            duration_hours = (self.out_time - self.in_time).total_seconds() / 3600
            # Per hour tarification
            if int(duration_hours) != duration_hours:
                duration_hours = int(duration_hours) + 1
            self.cost = duration_hours * self.car.fare

    # Cost calculation when saving the model
    def save(self, *args, **kwargs):
        self.calculate_cost()
        return super().save(*args, **kwargs)


class Ban(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Payment(models.Model):
    amount = models.FloatField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class ParkingInfo(models.Model):
    address = models.CharField(max_length=40, null=True)
    places = models.IntegerField(default=0)
    limit = models.FloatField(default=0)
    default_fare = models.FloatField(default=0)