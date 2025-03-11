from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models

# import from panel app
from .managers import UserManagerConfig

# import from extra modules
from extra_module.utils import username_validation, phone_validataion


class User(PermissionsMixin, AbstractBaseUser):
    username = models.CharField(_('نام کاربری'), max_length=60, validators=[username_validation],
        unique=True, blank=True, null=True
    )
    phone = models.CharField(_("شماره همراه"), max_length=11, unique=True, validators=[phone_validataion])
    email = models.EmailField(_("آدرس اینترنتی"), max_length=60, unique=True, blank=True, null=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManagerConfig()

    @property
    def is_staff(self):
        return self.is_admin
    

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'