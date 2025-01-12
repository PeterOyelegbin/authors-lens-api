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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import LogInView, TokenValidateView, ResetPassword, ConfirmResetPassword
from blog.views import BlogView

# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="AuthorsLens API",
      default_version='v2',
      description="AuthorsLens API is a Django-based server-side application that handles user authentication, blog management, and integration with a Cockroachdb database. It is built using Python, Django Rest Framework, and Djoser authentication, providing a robust and scalable foundation for blogging platforms.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(name="Peter Oyelegbin", url="https://peteroyelegbin.com.ng", email="info@peteroyelegbin.com.ng"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=False)
# router.register(r"accounts/signup", SignUpView, basename="signup")
router.register(r"login", LogInView, basename="login")
router.register(r"token/verify", TokenValidateView, basename="verify-otp")
# router.register(r"accounts/current", CurrentUser, basename="current")
router.register(r"users/reset_password", ResetPassword, basename="reset-password")
router.register(r"users/reset_password_confirm", ConfirmResetPassword, basename="confirm-password")
router.register(r"blogs", BlogView, basename="blogs")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    # API DOCS URL
    path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", include("djoser.urls")),
    # path("", include("djoser.urls.authtoken")),
]
