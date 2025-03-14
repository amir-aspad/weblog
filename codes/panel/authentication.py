from .models import User


class UsernameAuthenticate:
    def authenticate(self, request, phone=None, password=None):
        '''try login in user with username'''
        try:
            user = User.objects.get(username=phone)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailAuthenticate:
    def authenticate(self, request, phone=None, password=None):
        '''try login in user with email'''
        try:
            user = User.objects.get(email=phone)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None
        

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None