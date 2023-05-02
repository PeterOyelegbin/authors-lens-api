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
from rest_framework import routers
from accounts import views as acc_views
from blog import views as blg_views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r"accounts/signup", acc_views.SignUpView, basename="signup")
router.register(r"accounts/login", acc_views.LogInView, basename="login")
router.register(r"auth/token", acc_views.VerifyOTP, basename="verify-otp")
router.register(r"blogs", blg_views.BlogView, basename="blogs")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls))
]
