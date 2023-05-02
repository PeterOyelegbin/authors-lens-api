from django.db import models
from uuid import uuid4
from accounts.models import UserModel


# Create your models here.
class Blog(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True, db_index=True)
    cover_image = models.ImageField(upload_to="cumandra/images/")
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    # Sort post data in descending order
    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} || {self.author}"