from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# import from panel app
from .forms import LoginUserForm, RegisterUserForm, VerifyPhoneForm
from .models import User, OTP
from .mixins import MyLoginRequiredMixin

# import form module
from extra_module.utils import send_verify_phone

# import third module
from random import randint


class RegisterUserView(View):
    template_name = 'panel/register.html'
    form_class = RegisterUserForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you login. so you can not register')
            return redirect('panel:home')
        return super().dispatch(request, *args, **kwargs)

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
        messages.error(request, ' Please correct the errors below')
        return render(request, self.template_name, {'form':form})


class LoginUserView(View):
    template_name = 'panel/login.html'
    form_class = LoginUserForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'you login before')
            return redirect('panel:home')
        return super().dispatch(request, *args, **kwargs)

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
                return redirect(next if next else 'panel:home')
            else:
                messages.error(request, "your input info was wrong")

        return render(request, self.template_name, {'form':form})
    

class LogoutUserView(MyLoginRequiredMixin, View):
    def get(self, request):
        #TODO: The address of this method will be determined later.
        logout(request)
        return redirect('panel:home')


class HomeView(MyLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/home.html')
    

class VerifyPhoneView(View):
    form_class = VerifyPhoneForm
    template_name = 'panel/verify_phone.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_code = form.cleaned_data['code']
            info = request.session['user_registration_info']

            try:
                found_otp_code = OTP.objects.get(code=user_code, phone=info['phone'])

                if found_otp_code.is_alive():
                    # create user: user info in session object
                    user = User.objects.create(
                        phone = info['phone'],
                        password = info['password'],
                        verified_phone = True
                    )

                    # login registered user
                    login(request, user)

                    # delete user info from session
                    del info

                    # delete otp code
                    found_otp_code.delete()
                    
                    messages.success(request, 'your accounts was successfully created')
                    return redirect('panel:home')
                
                messages.error(request, 'code was expired')
                # delete otp code
                found_otp_code.delete()

            except OTP.DoesNotExist:
                messages.error(request, 'input code was wrong')
        return render(request, self.template_name, {'form':form})