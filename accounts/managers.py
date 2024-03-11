from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number=None, name=None, password=None):
        if not email:
            raise ValueError('User must have a valid email address')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number=None, name=None, password=None):
        user = self.create_user(email, phone_number, name, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
