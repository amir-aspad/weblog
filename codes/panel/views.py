from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.utils.text import slugify
from django.contrib import messages
from django.views import View

# import from blog app
from blog.models import Category

# import from panel app
from .forms import (
    LoginUserForm, RegisterUserForm, ChangeBaseInfoForm,
    VerifyPhoneForm, ChangeEmailForm, ChangePhoneForm,
    PostBlogForm
)
from .models import User, OTP
from .mixins import MyLoginRequiredMixin, AnonymousRequiredMixin, SendBlogPermissionMixin

# import form module
from extra_module.utils import send_verify_phone

# import third module
from random import randint


class RegisterUserView(AnonymousRequiredMixin, View):
    template_name = 'panel/register.html'
    form_class = RegisterUserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # generate verify code
            code = randint(100000, 999999)

            # save user info in session
            request.session['user_registration_info'] = {
                'phone':cd['phone'],
                'password':cd['password1']
            }

            # send verify code to user phone
            send_verify_phone(cd['phone'], code)

            # save code in otp model
            found_otp = OTP.objects.filter(phone=cd['phone'])
            if found_otp.exists():
                found_otp.delete()
            OTP.objects.create(phone=cd['phone'], code=code)

            messages.success(request, 'با موفقیت برای شماره همراه شما کد تایید ارسال شد')
            return redirect('panel:verify_phone')           
        messages.error(request, 'Please correct the errors below')
        return render(request, self.template_name, {'form':form})


class LoginUserView(AnonymousRequiredMixin, View):
    template_name = 'panel/login.html'
    form_class = LoginUserForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request, phone=cd['info'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'login successfully')

                next = request.GET.get('next', None)
                return redirect(next if next else 'panel:home_panel')
            else:
                messages.error(request, "your input info was wrong")

        return render(request, self.template_name, {'form':form})
    

class LogoutUserView(MyLoginRequiredMixin, View):
    def get(self, request):
        #TODO: The address of this method will be determined later.
        logout(request)
        return redirect('blog:blog_all')


class HomeView(MyLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/home.html')
    

class VerifyPhoneView(AnonymousRequiredMixin, View):
    form_class = VerifyPhoneForm
    template_name = 'panel/verify_phone.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code']
            self.info = request.session['user_registration_info']

            try:
                found_otp_code = OTP.objects.get(code=user_code, phone=self.info['phone'])

                if found_otp_code.is_alive():
                    # create user: user info in session object
                    user = User.objects.create(
                        phone = self.info['phone'],
                        password = self.info['password'],
                        phone_verified = True
                    )

                    # login registered user
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                    self.clear_data(found_otp_code)
                    
                    messages.success(request, 'your accounts was successfully created')
                    return redirect('panel:home_panel')
                
                messages.error(request, 'code was expired')
                self.clear_data(found_otp_code)

            except OTP.DoesNotExist:
                messages.error(request, 'input code was wrong')
        return render(request, self.template_name, {'form':form})
    

    def clear_data(self, otp):
        '''create session and delete otp code'''
        # clear session
        del self.info
        # delete otp code
        otp.delete()


class ChangePhoneUser(MyLoginRequiredMixin, View):
    template_name = 'panel/change_phone.html'
    form_class = ChangePhoneForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.phone_verified = False
            user.save()
            messages.success(request, 'your phone succeesfully change')
            return redirect('panel:home_panel')
        messages.error(request, 'Please correct the errors below')
        return render(request, self.template_name, {'form':form})
    

class ChangeEmailUser(MyLoginRequiredMixin, View):
    template_name = 'panel/change_email.html'
    form_class = ChangeEmailForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        return render(request, self.template_name, {'form':form})
    

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.save()
            messages.success(request, 'your email succeesfully change')
            return redirect('panel:home_panel')
        messages.error(request, 'Please correct the errors below')
        return render(request, self.template_name, {'form':form})
    

class ChangeBaseInfoView(MyLoginRequiredMixin, View):
    template_name = 'panel/change_info.html'
    form_class = ChangeBaseInfoForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'username':request.user.username})
        return render(request, self.template_name, {'form':form})
    
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            user = form.save(commit=False)
            user.user.username = form.cleaned_data['username']
            user.save()
            user.user.save()
            messages.success(request, 'your info save successfully')
            return redirect('panel:home_panel')
        messages.error(request, 'Please correct the errors below')
        return render(request, self.template_name, {'form':form})


class PostBlogView(MyLoginRequiredMixin, SendBlogPermissionMixin, View):
    from_class = PostBlogForm
    template_name = 'panel/post_blog.html'

    def get(self, request):
        form = self.from_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.from_class(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.slug = slugify(form.cleaned_data['title'], allow_unicode=True)

            blog.save()
            cates_title = [cate.title for cate in form.cleaned_data['cates']]
            blog.cates.set(Category.objects.filter(title__in=cates_title))
            
            messages.success(request, 'your blog create successfully')
            return redirect('panel:home_panel')

        messages.error(request, 'Please correct the errors below')
        return render(request, self.template_name, {'form':form})