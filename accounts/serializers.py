from rest_framework import serializers
from .models import UserModel


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "first_name", "last_name", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        instance.email = instance.email.lower()
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = ("email", "password")


class OTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_token = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = ("email", "otp_token")


class PasswordReset(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email")


class ConfirmPasswordReset(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = ("email", "token", "password")
