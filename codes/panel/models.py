from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

# import from panel app
from .managers import UserManagerConfig


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('نام کاربری'), max_length=60, unique=True, blank=True, null=True)
    phone = models.CharField(_("شماره همراه"), max_length=11, unique=True)
    email = models.EmailField(_("آدرس اینترنتی"), max_length=60)

    is_admin = models.BooleanField()
    is_active = models.BooleanField()

    USERNAME_FILED = 'phone'
    REQUIRED_FIELDS = [username, email]

    objects = UserManagerConfig()

    @property
    def is_staff(self):
        return self.is_admin