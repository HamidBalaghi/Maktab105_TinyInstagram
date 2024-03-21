from django.db import models

from accounts.models import Profile


# Create your models here.


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    publish_at = models.DateTimeField(auto_now_add=True)
    publishable = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.profile} - {self.id}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='static/postImages')

    def __str__(self):
        return f'{self.post} - {self.id}'
