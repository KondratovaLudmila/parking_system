from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from parking.models import Park, Payment
from utils.mailing import debtor_notification
from utils.parkingsend import tg_notify


@receiver(post_save, sender=Park)
def debiting(sender, instance, created, **kwargs):
    """
    The debiting function is called when a new instance of the CarWash model is created.
    It checks if there are any payments for the user who owns the car that was washed, and if so, 
    it subtracts from his balance (payment.amount) by an amount equal to cost of washing (instance.cost). 
    If after this operation payment's amount becomes negative, it sends a notification to debtor.
    
    :param sender: Determine the model that is sending the signal
    :param instance: Access the instance of the model that is being saved
    :param created: Check if the object is created or updated
    :param **kwargs: Pass keyworded, variable-length argument list to a function
    :return: Nothing
    :doc-author: Trelent
    """
    if not created:
        payment = Payment(amount=-instance.cost, user=instance.car.user)
        payment.save()
    #Notify user in telegram
    tg_notify(instance.car.user.email)


@receiver(post_save, sender=Payment)
def balance_correction(sender, instance, created, **kwargs):
    if instance.amount == 0:
        return
    
    profile = instance.user.profile
    if not profile:
        return
    
    profile.balance += instance.amount
    profile.save()

    if profile.balance < 0:
        debtor_notification(profile.user, profile.balance)