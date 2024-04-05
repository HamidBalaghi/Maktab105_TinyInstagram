from django.db import models
from django.utils.text import slugify

from accounts.models import Profile
from posts.models import Post


# Create your models here.

class Like(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)


class Comment(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_deleted = models.BooleanField(default=False)


class Hashtag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    posts = models.ManyToManyField(Post, related_name='hashtags')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
