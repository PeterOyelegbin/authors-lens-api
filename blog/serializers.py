from rest_framework import serializers
from .models import Blog, UserModel


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="pen_name", queryset=UserModel.objects.all())

    class Meta:
        model = Blog
        fields = "__all__"
