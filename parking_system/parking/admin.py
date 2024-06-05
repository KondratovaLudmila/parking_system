from django.contrib import admin
from .models import Car, Park, Ban


# Register your models here.
admin.site.register(Car)
admin.site.register(Park)
admin.site.register(Ban)
