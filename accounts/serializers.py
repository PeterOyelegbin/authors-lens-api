from rest_framework import serializers


class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        fields = ("email", "password")
    

class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ("token")


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
