from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django import forms

# import from panel app
from .models import User


class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label=_('پسورد'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("تکرار پسورد"), widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ['phone', 'username', 'email', 'password1', 'password2']

    
    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']

        if p1 and p2 and p1 != p2:
            raise ValidationError('پسورد ها باید یکسان باشد')
        
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text='for change password use this <a href="../password">link</a>')

    class Meta:
        models = User
        fields = '__all__'


class LoginUserForm(forms.Form):
    info = forms.CharField(
        label=_('شماره همراه، یوزر نیم یا ایمیل'),
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password = forms.CharField(
        label=_('پسورد'),
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )


class RegisterUserForm(forms.Form):
    phone = forms.CharField(label=_("شماره همراه"), max_length=11)
    password1 = forms.CharField(label=_("پسورد"), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_("تکرار پسورد"), widget=forms.PasswordInput())

    def clean_password2(self):
        p1 = self.cleaned_data['password1']
        p2 = self.cleaned_data['password2']

        if p1 and p2 and p1 != p2:
            raise ValidationError('پسورد ها باید یکسان باشد')
        
        return p2
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise ValidationError('این شماره همراه از قبل وجود دارد')
        
        return phone
    

class VerifyPhoneForm(forms.Form):
    code = forms.CharField(label=_('کد تایید'))