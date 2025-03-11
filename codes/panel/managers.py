from django.contrib.auth.models import BaseUserManager


class UserManagerConfig(BaseUserManager):
    def create_user(self, phone, username, email, password):
        if not phone:
            raise ValueError('phone is required')

        if not password:
            raise ValueError('password is required')
        
        user = self.model(
            phone=phone,
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    
    def create_superuser(self, phone, username, email, password):
        user = self.create_user(phone, username, email, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user