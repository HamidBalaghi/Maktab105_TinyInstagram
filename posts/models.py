from django.db import models

from accounts.models import Profile


# Create your models here.


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    publish_at = models.DateTimeField(auto_now_add=True)
    publishable = models.BooleanField(default=True)
