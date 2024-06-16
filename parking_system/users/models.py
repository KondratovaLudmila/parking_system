from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tg_token = models.CharField(max_length=30, null=False)
    balance = models.fields.FloatField(default=0)

    def __str__(self):
        return self.user.username
