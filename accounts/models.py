from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
import random


class User(AbstractBaseUser):
    email = models.CharField(max_length=100, unique=True, validators=[
        RegexValidator(
            regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            message='Enter a valid email address'
        )
    ])
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True, validators=[
        RegexValidator(
            regex='^09\d{9}$',
            message='Phone number must be 11 digits starting with "09"'
        )
    ])
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)
    image = models.ImageField(null=True, blank=True, upload_to='media/profile_pics')
    created_at = models.DateTimeField(auto_now_add=True)
    about_me = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)

    def get_followings(self):
        temp = self.followings.all()
        followers = []
        for user in temp:
            followers.append(user.following.user)
        return followers

    def get_followers(self):
        temp = self.followers.all()
        followings = []
        for user in temp:
            followings.append(user.profile.user)
        return followings

    def __str__(self):
        return self.user.name


class Follow(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')
    accepted = models.BooleanField(default=False)
    follow_at = models.DateTimeField(auto_now_add=True)
    close_friend = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.profile == self.following:
            raise ValueError("A user cannot follow themselves.")
        if self.accepted is None:
            self.accepted = self.following.is_public
        super(Follow, self).save(*args, **kwargs)
