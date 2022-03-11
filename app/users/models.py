from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    pass


class Profile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # type: CustomUser

    def __str__(self):
        return self.user.username



