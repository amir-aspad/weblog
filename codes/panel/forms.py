from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms

# import from panel app
from .models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(_('پسورد'), widget=forms.PasswordInput)
    password2 = forms.CharField(_("تکرار پسورد"), widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ['phone', 'username', 'email', 'password1', 'password2']

    
    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']

        if p1 and p2 and p1 != p2:
            raise ValidationError('پسورد ها باید یکسان باشد')


    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        models = User
        fields = [
            'phone', 'username', 'email', 'password',
            'is_active', 'is_admin', 'is_superuser',
            'groups', 'user_permissions'
        ]