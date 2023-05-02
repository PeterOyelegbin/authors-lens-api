from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from .managers import UserModelManager


# Create your models here.
class UserModel(AbstractUser):
    username = None
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    pen_name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    otp_token = models.CharField(max_length=6, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserModelManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
