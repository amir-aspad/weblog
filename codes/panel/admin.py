from typing import Any
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from django.forms.models import ModelForm
from django.http import HttpRequest

from .forms import UserChangeForm, UserCreateForm
from .models import User


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreateForm

    fieldsets = (
        (None, {'fields': ('phone', 'username', 'email', 'password')}),
        ('permissions', {'fields': ('groups', 'user_permissions', 'is_admin', 'is_active', 'is_superuser')}),
        ('date', {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {'fields': ('phone', 'username', 'email', 'password1', 'password2')}),
    )

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
    

admin.site.register(User, UserAdmin)