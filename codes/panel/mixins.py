from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

# import from blog app
from blog.models import Blog


class MyLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            next_url = request.GET.get('next', request.path)
            messages.error(request, "You should login first!")
            return redirect(f'{reverse("panel:login")}?next={next_url}')
        return super().dispatch(request, *args, **kwargs)
    

class AnonymousRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'You are logged in so you cannot access that page.')
            return redirect('panel:home_panel')
        return super().dispatch(request, *args, **kwargs)
    

class SendBlogPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.phone_verified:
            messages.error(
                request,
                'For creating a blog, your phone should be verify'
            )
            return redirect('panel:home_panel')
        if not request.user.username:
            messages.error(
                request,
                f'For creating a blog, you should add your username. Do it <a href="{reverse("panel:change_info")}">here</a>'
            )
            return redirect('panel:home_panel')
        return super().dispatch(request, *args, **kwargs)
    

class OwnerBlogMixin:
    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, pk=kwargs['blog_id'])
        if self.blog.author != request.user:
            messages.error(request, 'you have no access to this blog')
            return redirect('panel:my_blog')
        return super().dispatch(request, *args, **kwargs)