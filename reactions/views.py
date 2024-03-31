from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from posts.models import Post
from .models import Like


# Create your views here.

class LikeView(View):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post_owner = post.profile
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('accounts:login')
        if not request.user.profile.is_active or not post.is_active or not post.publishable:
            raise PermissionDenied
        if not post_owner.is_public and request.user.profile not in post_owner.get_followers:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        try:
            reaction = Like.objects.get(profile=request.user.profile, post=post)
            if ('/like/' in request.path and reaction.liked) or ('/dislike/' in request.path and reaction.disliked):
                reaction.delete()
            elif '/like/' in request.path:
                reaction.liked = True
                reaction.disliked = False
                reaction.save()
            else:
                reaction.liked = False
                reaction.disliked = True
                reaction.save()

        except Like.DoesNotExist:
            reaction = Like(profile=request.user.profile, post=post)
            if '/like/' in request.path:
                reaction.liked = True
            else:
                reaction.disliked = True
            reaction.save()

        return redirect('post:post', pk=post.pk)
