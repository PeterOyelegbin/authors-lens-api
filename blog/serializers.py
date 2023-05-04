from rest_framework import serializers
from .models import Blog
from accounts.serializers import LogInSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = LogInSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = "__all__"

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.author = self.context['request'].user
        instance.save()
        return instance
