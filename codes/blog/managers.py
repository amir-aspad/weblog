from django.contrib.auth.models import BaseUserManager


class PostManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)