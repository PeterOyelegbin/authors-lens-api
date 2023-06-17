from django.contrib import admin
from .models import Blog


# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_on")
    list_filter = ("updated_on",)
