from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email=None, name=None, password=None):
        if not phone_number:
            raise ValueError('User must have a phone number')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email=None, name=None, password=None):
        user = self.create_user(phone_number, email, name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator(
            regex='^09\d{9}$',
            message='Phone number must be 11 digits starting with "09"'
        )
    ])
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'name']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
