from rest_framework import serializers
from accounts.serializers import SignUpSerializer
from .models import Blog


class BlogSerializer(serializers.ModelSerializer):
    author = SignUpSerializer()

    class Meta:
        model = Blog
        fields = "__all__"
