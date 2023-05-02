from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserModel
from .serializers import SignUpSerializer, LogInSerializer, OTPSerializer
from pyotp import random_base32, HOTP
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class SignUpView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ["post", "head"]


class LogInView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = LogInSerializer
    http_method_names = ["post", "head"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        email = data.get("email", None)
        password = data.get("password", None)
        if (email == "") or (password == ""):
            return Response({"Message": "Email and Password fields are required"}, 400)
        user = authenticate(username=email.lower(), password=password)
        if user is None:
            return Response({"Message": "Incorrect email or password"}, 401)
        if not user.check_password(password):
            return Response({"Message": "Incorrect email or password"}, 401)

        # generate the token and save in database
        otp_base32 = random_base32()
        token = HOTP(otp_base32)
        user.otp_token = token.at(0)
        user.save()

        # send the token to the user email
        send_mail(
            subject="AuthorsLens: Login Token",
            message=f"Hello {user.first_name} {user.last_name}, your AuthorsLens login token is {user.otp_token} and expires in 10 minutes. Thank you",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response({"Message": "OTP sent to your email"}, 200)


class VerifyOTP(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = OTPSerializer
    http_method_names = ["post", "delete", "head"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        email = data.get("email")
        otp_token = data.get("otp_token")
        if (email == "") or (otp_token == ""):
            return Response({"Message": "Email and OTP fields are required"}, 400)
        user = self.queryset.filter(email=email).first()
        if user is None:
            return Response({"Message": f"No user with email: {email}"}, 404)
        if otp_token != user.otp_token:
            return Response({"Message": "Invalid token"}, 400)
        login(request, user)
        user.otp_token = ""
        user.save()
        serializer = self.serializer_class(user)
        return Response({"Message": "OTP verified successfully", "user": serializer.data}, 202)

    def destroy(self, request, *args, **kwargs):
        logout(request)
        return Response({"Message": "Logged out successfully!"}, 200)
