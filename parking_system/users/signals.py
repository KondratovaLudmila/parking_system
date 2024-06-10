from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from parking.models import Payment, ParkingInfo


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        parking = ParkingInfo.objects.first()
        Payment.objects.create(user=instance, amount=parking.limit)