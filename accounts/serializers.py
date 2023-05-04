from rest_framework import serializers
from .models import UserModel


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "email", "phone", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LogInSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "first_name", "last_name", "email", "password"]
        extra_kwargs = {
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "password": {"write_only": True},
        }


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ["id", "email", "otp_token"]
        extra_kwargs = {"otp_token": {"write_only": True}}
