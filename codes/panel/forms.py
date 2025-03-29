from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django import forms

# import from blog app
from blog.models import Blog, Category

# import from panel app
from .models import User, Profile

# import forom module
from extra_module.utils import phone_validataion, username_validation


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
        label=_('phone or username or email'),
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))


class RegisterUserForm(forms.Form):
    phone = forms.CharField(
        max_length=11, validators=[phone_validataion],
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password1 = forms.CharField(
        label=_("password"),      
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )
    password2 = forms.CharField(
        label=_("password confirm"),
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

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
    code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    

class ChangePhoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone',)
        widgets = {
            'phone':forms.TextInput(attrs={'class':'form-control'})
        }


    def clean_phone(self):
        phone = self.cleaned_data['phone']

        if User.objects.filter(phone=phone).exists():
            raise ValidationError('this phone already exists')

        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        user.phone_verified = False
        if commit:
            user.save()
        return user
    

class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control'})
        }


    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists():
            raise ValidationError('this email already exists')

        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email_verified = False
        if commit:
            user.save()
        return user
    

class ChangeBaseInfoForm(forms.ModelForm):
    username = forms.CharField(
        label=_("نام کاربری"), validators=[username_validation],
        widget=forms.TextInput(attrs={'class':'form-control'})
    )
    profile = forms.ImageField(label=_("پروفایل"))
    
    class Meta:
        model = Profile
        fields = ('profile', 'first_name', 'last_name', 'bio', 'username')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def save(self, form, commit=True):
        profile = super().save(commit=False)
        profile.user.username = form['username']
        if commit:
            profile.save()
            profile.user.save()
        return profile


    def clean_username(self):
        username = self.cleaned_data['username']
        

        if self.instance.user.username != username:
            if User.objects.filter(username=username).exists():
                raise ValidationError('this username already exists')
        
        return username
    

class PostBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'baner', 'text', 'cates')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'text': forms.Textarea(attrs={'class':'form-control'}),
            'baner': forms.FileInput(attrs={'class':'form-control'}),
            'cates': forms.SelectMultiple(attrs={'class':'form-control'}),
        }


    def save(self, request, form, commit=True):
        blog = super().save(commit=False)
        blog.author = request.user
        blog.slug = slugify(form['title'], allow_unicode=True)

        if commit:
            blog.save()
        cates_title = [cate.title for cate in form['cates']]
        blog.cates.set(Category.objects.filter(title__in=cates_title))
        return blog