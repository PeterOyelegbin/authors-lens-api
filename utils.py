from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
import logging


"""
Custom user model manager where email is the unique identifiers
for authentication instead of usernames.
"""
class UserModelManager(BaseUserManager):
    # Create and save a user with the given email and password.
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # Create and save a SuperUser with the given email and password.
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
    

# Get the email and general error logger
email_logger = logging.getLogger('email_logger')
general_logger = logging.getLogger('general_logger')


# Asynchronous email sending
def send_async_email(email_subject, email_body, email_recipient, email_headers=None):
    try:
        email_sender = settings.DEFAULT_FROM_EMAIL
        email = EmailMultiAlternatives(email_subject, email_body, email_sender, email_recipient, headers=email_headers)
        email.send()
    except Exception as e:
        email_logger.error(f"Error sending email: {e}")
