from django.contrib.auth.models import User
from django.core.mail import send_mail

def debtor_notification(debtor: User, debt: float):
    if not debtor.email:
        return
    message = f'Hello, dear {debtor.username}!\n\
                Please be advised of a {abs(debt)} parking debt.\n\
                Repay this debt as soon as possible, otherwise you will not be able to share our services.\n\
                With best regards, Parking Administrator.'
    send_mail('Parking debt warning', message, from_email=None, recipient_list=[debtor.email,])