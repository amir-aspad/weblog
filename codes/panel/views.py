from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View

# import from panel app
from .forms import LoginUserForm


class LoginUserView(View):
    template_name = 'panel/login.html'
    form_class = LoginUserForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'شما قبلا وارد شدید')
            return redirect('panel:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            user = authenticate(request, username=cd['info'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'با موفقیت وارد شدید')

                next = request.GET.get('next', None)
                return redirect(next if next else 'panel:home')
            else:
                messages.error(request, "اطلاعات وارد شده درست نمی‌باشد")

        return render(request, self.template_name, {'form':form})
    

class LogoutUserView(LoginRequiredMixin, View):
    def get(self, request):
        #TODO: The address of this method will be determined later.
        logout(request)
        return redirect('panel:')


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'panel/home.html')