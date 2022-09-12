from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Post


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

class PostSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    class Meta:
        model = Post
        fields = ['author', 'image', 'title', 'content']
