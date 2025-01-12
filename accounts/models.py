from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
from utils import UserModelManager


# Create your models here.
class UserModel(AbstractUser):
    """
    This model will serve as the default authentication model via AUTH_USER_MODEL in settings.py
    """
    username = None
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserModelManager()

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    