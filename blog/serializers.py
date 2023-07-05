from rest_framework import serializers
from djoser.serializers import UserSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(write_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"
