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

    # verify phone or email is boolean
    verified_phone = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)

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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.ImageField(_("پروفایل"), upload_to='user', blank=True, null=True)
    bio = models.TextField(_('توضیحات'), max_length=120, blank=True, null=True)
    first_name = models.CharField(_('نام'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('نام خانوادگی'), max_length=30, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

