from rest_framework import serializers
from .models import Blog, UserModel


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field="pen_name", queryset=UserModel.objects.all())
    # author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    
    # def create(self, validated_data):
    #     blog = Blog(
    #         author = self.context['request'].user,
    #         menu_item_id=validated_data['menu_item_id'],
    #         quantity=validated_data['quantity'],
    #     )
    #     blog.save()
    #     return blog

    class Meta:
        model = Blog
        fields = "__all__"

    # def create(self, validated_data):
    #     instance = self.Meta.model(**validated_data)
    #     instance.author = self.context['request'].user
    #     instance.save()
    #     return instance