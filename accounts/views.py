from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, tokens
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
from .models import UserModel
from .serializers import SignUpSerializer, LogInSerializer, TokenSerializer, PasswordReset, ConfirmPasswordReset


# Create your views here.
class AuthView(viewsets.ViewSet):
    def list(self, request):
        routes = {
            "signup": "https://authorslens-api.vercel.app/users",
            "user": "https://authorslens-api.vercel.app/users/me",
            "login": "https://authorslens-api.vercel.app/login",
            "token": "https://authorslens-api.vercel.app/token/verify",
            "logout": "https://authorslens-api.vercel.app/token/logout",
            "reset-password": "https://authorslens-api.vercel.app/users/reset_password",
            "confirm-password-reset": "https://authorslens-api.vercel.app/users/reset_password_confirm",
        }
        return Response(routes, 200)


class LogInView(viewsets.GenericViewSet):
    serializer_class = LogInSerializer
    http_method_names = ["post"]

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        password = data["password"]
        user = authenticate(username=email.lower(), password=password)
        if user is None:
            return Response({"Message": "Incorrect email or password"}, 401)
        # generate token
        token, _ = Token.objects.get_or_create(user_id=user.id)
        # send the token to the user email
        send_mail(
            subject="AuthorsLens: Login Token",
            message=f"Dear {user.first_name} {user.last_name},\n\nYour AuthorsLens login token is {token} and expires in 10 minutes.\n\nThank you,\nAuthorsLens",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return Response({"Message": "Token sent to your email"}, 200)


class TokenValidateView(viewsets.GenericViewSet):
    serializer_class = TokenSerializer
    http_method_names = ["post"]

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        token = data["token"]
        token = Token.objects.filter(key=token).first()
        if token:
            return Response({"token": token.key, "user": token.user_id}, 200)
        return Response({'Error': 'Invalid token!'}, 401)


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
