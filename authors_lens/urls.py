"""authors_lens URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AuthView, LogInView, TokenValidateView, ResetPassword, ConfirmResetPassword
# from rest_framework.authtoken.views import ObtainAuthToken
from blog.views import BlogView


router = DefaultRouter(trailing_slash=False)
router.register(r"auths", AuthView, basename="auth")
# router.register(r"accounts/signup", SignUpView, basename="signup")
# router.register(r"accounts/login", LogInView, basename="login")
# router.register(r"accounts/auth-otp", VerifyOTP, basename="verify-otp")
# router.register(r"accounts/current", CurrentUser, basename="current")
# router.register(r"accounts/password-reset", ResetPassword, basename="password_reset")
# router.register(r"accounts/password-reset/confirm", ConfirmResetPassword, basename="password_reset_confirm")
router.register(r"blogs", BlogView, basename="blogs")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    # path("token-auth", obtain_auth_token),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.authtoken")),
    path("login", LogInView.as_view({'post': 'create'}), name="login"),
    path("token/verify", TokenValidateView.as_view({'post': 'create'}), name="verify-token"),
]
