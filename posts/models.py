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

    def get_comments(self):
        comments = []
        for comment in self.comments.filter(is_deleted=False):
            temp = {}
            temp['owner'] = comment.profile
            temp['text'] = comment.comment
            temp['date'] = comment.created_at
            temp['parent'] = comment.parent_comment
            temp['image'] = comment.profile.get_image_url
            temp['comment_id'] = comment.pk
            comments.append(temp)
        return comments

    def get_reactions(self):
        reaction = {}

        likes = self.reactions.filter(liked=True).select_related('profile')
        reaction['likes'] = [like.profile for like in likes]
        reaction['like_count'] = len(likes)

        dislikes = self.reactions.filter(disliked=True).select_related('profile')
        reaction['dislikes'] = [dislike.profile for dislike in dislikes]
        reaction['dislike_count'] = len(dislikes)

        return reaction

    def user_reaction(self, user):
        try:
            like_reaction = self.reactions.get(profile=user)
            if like_reaction.liked:
                return 'liked'
            elif like_reaction.disliked:
                return 'disliked'
        except:
            return 'no_reaction'

    def __str__(self):
        return f'{self.profile} - {self.id}'


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.post} - {self.id}'
