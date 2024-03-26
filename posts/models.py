from django.db import models

from accounts.models import Profile


# Create your models here.


class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    publish_at = models.DateTimeField(auto_now_add=True)
    publishable = models.BooleanField(default=True)

    def get_images(self):
        images = self.images.all()
        return images

    def first_image(self):
        return self.images.first()

    def __str__(self):
        return f'{self.profile} - {self.id}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.post} - {self.id}'
