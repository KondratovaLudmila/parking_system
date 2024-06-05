from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    reg_mark = models.CharField(max_length=8, null=False, unique=True)
    model = models.CharField(max_length=30, null=False)
    color = models.CharField(max_length=30, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reg_mark}"


class Park(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField()


class Ban(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
