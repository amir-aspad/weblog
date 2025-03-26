from django.contrib.auth.models import BaseUserManager


class ActiveManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
    

class FristCommentManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True, is_reply=False)