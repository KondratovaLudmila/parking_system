from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from parking.models import Payment, Park


@receiver(post_save, sender=Park)
def debiting(sender, instance, created, **kwargs):
    if not created:
        payment = Payment.objects.filter(user=instance.car.user).first()
        if payment:
            payment.amount -= instance.cost
            payment.save()