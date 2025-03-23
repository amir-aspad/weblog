from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class MyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.GET.get('next', request.path)
            messages.error(request, "You should login first!")
            
            return redirect(f'{reverse("panel:login")}?next={next_url}')
        return super().dispatch(request, *args, **kwargs)