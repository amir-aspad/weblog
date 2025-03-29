from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.views import View


class MyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.GET.get('next', request.path)
            messages.error(request, "You should login first!")
            return redirect(f'{reverse("panel:login")}?next={next_url}')
        return super().dispatch(request, *args, **kwargs)
    

class AnonymousRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are logged in so you cannot access that page.')
            return redirect('panel:home_panel')
        return super().dispatch(request, *args, **kwargs)
    

class SendBlogPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.phone_verified:
            messages.error(request, 'for send blog. your phone should verify')
            return redirect('panel:home_panel')
        if not request.user.username:
            messages.error(request, 'for send blog. you should have username')
            return redirect('panel:home_panel')
        return super().dispatch(request, *args, **kwargs)