from django.db import models
from uuid import uuid4
from accounts.models import UserModel
from ckeditor.fields import RichTextField


# Create your models here.
category_option = [
    ("Technology", "Technology"),
    ("Lifestyle", "Lifestyle"),
    ("Relationship", "Relationship"),
    ("Others", "Others"),
]

class Blog(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=225, unique=True, db_index=True)
    cover_image = models.ImageField(upload_to="authorslens/images/")
    category = models.CharField(max_length=20, choices=category_option, default="Others")
    content = RichTextField()
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

    # Sort post data in descending order
    class Meta:
        ordering = ["-updated_on"]

    def __str__(self):
        return f"{self.title} || {self.author}"
