from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, tokens
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import UserModel
from .serializers import SignUpSerializer, LogInSerializer, OTPSerializer, PasswordReset, ConfirmPasswordReset
from pyotp import random_base32, HOTP
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class SignUpView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        # send mail for successful account creation
        send_mail(
            subject="AuthorsLens: User Created",
            message=f"Dear {data['first_name']} {data['last_name']},\n\nCongratulations! Your account has been created successfully on AuthorsLens platform, click the link below to login and unleash your ideas.\n\nhttps://authorslens.netlify.app/\n\nCheers,\nAuthorsLens",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[data['email']],
        )
        serializer.save()
        return Response(serializer.data, 200)


class LogInView(viewsets.GenericViewSet):
    serializer_class = LogInSerializer
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        password = data["password"]
        user = authenticate(username=email.lower(), password=password)
        if user is None:
            return Response({"Message": "Incorrect email or password"}, 401)
        # erase previous otp
        user.otp_token = None
        user.save()
        
        # generate new token
        otp_base32 = random_base32()
        token = HOTP(otp_base32)
        otp = token.at(0)
        
        # send the token to the user email
        send_mail(
            subject="AuthorsLens: Login Token",
            message=f"Dear {user.first_name} {user.last_name},\n\nYour AuthorsLens login token is {otp} and expires in 10 minutes.\n\nThank you,\nAuthorsLens",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        # save token
        user.otp_token = otp
        user.save()
        return Response({"Message": "OTP sent to your email"}, 200)


class VerifyOTP(viewsets.GenericViewSet):
    serializer_class = OTPSerializer
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        otp_token = data["otp_token"]
        user = UserModel.objects.filter(email=email).first()
        if user is None:
            return Response({"Message": f"No user with email: {email}"}, 400)
        if otp_token != user.otp_token:
            return Response({"Message": "Invalid token"}, 401)
        login(request, user)
        user.otp_token = None
        user.save()
        return Response({"Message": "OTP verified successfully"}, 202)


class ResetPassword(viewsets.GenericViewSet):
    serializer_class = PasswordReset
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = UserModel.objects.filter(email=email).first()
        if not user:
            return Response({"Message": "User does not exist!"}, 400)
        token = tokens.PasswordResetTokenGenerator().make_token(user)
        send_mail(
            subject="AuthorsLens: Password Reset",
            message=f"You initiated a password reset process for your AuthorsLens account, please copy and paste the reset token= {token} in the link below:\n\nhttps://authorslens.netlify.app/password-reset/confirm\n\nPS: Please ignore if you did not initiate this process\n\nRegards,\nAuthorsLens",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response({"Message": "Password reset token sent to your email"}, 200)
        

class ConfirmResetPassword(viewsets.GenericViewSet):
    serializer_class = ConfirmPasswordReset
    http_method_names = ["post"]

    @method_decorator(csrf_exempt)
    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        token = serializer.data["token"]
        password = data["password"]
        user = UserModel.objects.get(email=email)
        if not user:
            return Response({"Message": "User does not exist!"}, 400)
        if not tokens.PasswordResetTokenGenerator().check_token(user, token):
            return Response({"Message": "The reset token is invalid!"}, 400)
        user.set_password(password)
        user.save()
        return Response({"Message": "Password reset complete"}, 200)
