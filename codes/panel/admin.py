from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

from .forms import UserChangeForm, UserCreateForm
from .models import User, Profile, OTP


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'پروفایل ها'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        (None, {'fields': ('phone', 'username', 'email', 'password')}),
        ('permissions', {'fields': ('groups', 'user_permissions', 'is_admin', 'is_active', 'is_superuser')}),
        ('verify', {'fields': ('verified_email', 'verified_phone')}),
        ('date', {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'username', 'email', 'password1', 'password2')}),
    )
    inlines = (ProfileInline, )

    list_display = ('phone', 'username', 'email', 'is_active')
    list_filter = ('is_active', 'is_admin')
    search_fields = ('phone', 'username', 'eamil')
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ('last_login',)


    def get_form(self, request, obj=None, **kwargs) :
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone', 'code', 'created')
    