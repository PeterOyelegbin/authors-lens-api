from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from threading import Thread
from utils import send_async_email, general_logger
from .serializers import LogInSerializer, TokenSerializer


# Create your views here.
class LogInView(viewsets.ViewSet):
    """
    Login Endpoint

    User log in with their email and password.
    """
    serializer_class = LogInSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(request_body=LogInSerializer, responses={200: 'OK', 400: 'BAD_REQUEST', 401: 'UNAUTHORIZED'})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(username=email, password=password)
            if user:
                # generate token
                token, _ = Token.objects.get_or_create(user=user)
                # send the token to the user email
                email_subject = 'AuthorsLens: Login Token'
                email_body = f"""Dear {user},\n\nYour AuthorsLens login token is {token} and expires in 10 minutes.\n\nRegards,\nAuthorsLens"""
                recipient = [user.email]
                # Asynchronously handle send mail
                Thread(target=send_async_email, args=(email_subject, email_body, recipient)).start()
                response_data = {
                    'success': True,
                    'status': 200,
                    'message': 'Login token sent to your email'
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    'success': False,
                    'status': 401,
                    'message': 'Invalid credentials',
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 400,
                'message': 'Email or password field is invalid or empty',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

class TokenValidateView(viewsets.ViewSet):
    """
    Login Token Validation Endpoint

    User validate login token.
    """
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=TokenSerializer, responses={200: 'OK', 400: 'BAD_REQUEST', 500: 'INTERNAL_SERVER_ERROR'})
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:    
            serializer.is_valid(raise_exception=True)
            otp = serializer.validated_data.get('token')
            token = Token.objects.get(key=otp)
            token.delete()
            response_data = {
                'success': True,
                'status': 200,
                'message': 'Login sucessful!',
                'token': token.key,
                'user': token.user_id
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            response_data = {
                'success': False,
                'status': 400,
                'message': 'Invalid token!',
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            general_logger.error("An error occurred: %s", e)
            response_data = {
                'success': False,
                'status': 500,
                'message': 'An error occurred, kindly contact support',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        