from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import DetailView

from accounts.models import Profile, Follow
from core.mixin import LoginRequiredMixin, NavbarMixin
from posts.models import Post
from .models import Like, Comment
from django.http import JsonResponse


# Create your views here.

class LikeView(View):
    def dispatch(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        post_owner = post.profile
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('accounts:login')
        if not request.user.profile.is_active or not post.is_active or not post.publishable:
            raise PermissionDenied
        if not post_owner.is_public and request.user.profile not in post_owner.get_followers and post_owner != request.user.profile:
            print('2')
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        try:
            reaction = Like.objects.get(profile=request.user.profile, post=post)
            if ('/like/' in request.path and reaction.liked) or ('/dislike/' in request.path and reaction.disliked):
                reaction.delete()
                return JsonResponse({'response': 'no_reaction'})
            elif '/like/' in request.path:
                reaction.liked = True
                reaction.disliked = False
                reaction.save()
                return JsonResponse({'response': 'liked'})
            else:
                reaction.liked = False
                reaction.disliked = True
                reaction.save()
                return JsonResponse({'response': 'disliked'})

        except Like.DoesNotExist:
            reaction = Like(profile=request.user.profile, post=post)
            if '/like/' in request.path:
                reaction.liked = True
                reaction.save()
                return JsonResponse({'response': 'new_liked'})
            else:
                reaction.disliked = True
                reaction.save()
                return JsonResponse({'response': 'new_disliked'})


class FollowView(View):
    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, pk=kwargs['pk'])
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('accounts:login')

        if not request.user.profile.is_active or not self.profile.is_active or request.user.profile == self.profile:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if '/follow/' in request.path:
            follow, created = Follow.objects.get_or_create(profile=request.user.profile, following=self.profile)
            return JsonResponse({'response': 'followed'})
        else:
            try:
                Follow.objects.get(profile=request.user.profile, following=self.profile).delete()
                return JsonResponse({'response': 'unfollowed'})
            except:
                raise PermissionDenied


class DeleteComment(View):
    def dispatch(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])

        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('accounts:login')
        post_owner = comment.post.profile
        if not request.user.profile.is_active or not post_owner.is_active:
            raise PermissionDenied

        commenter = comment.profile
        if request.user.profile != commenter and request.user.profile != post_owner:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        post_id = comment.post.pk
        comment.is_deleted = True
        comment.save()
        return redirect('post:post', pk=post_id)


class ShowLikes(LoginRequiredMixin, NavbarMixin, DetailView):
    model = Post
    template_name = 'profile/follow.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        self.post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        post_owner = self.post.profile
        if not request.user.is_authenticated or request.user.is_anonymous:
            return redirect('accounts:login')
        user = request.user.profile
        if not post_owner.is_active or not user.is_active or not self.post.is_active:
            raise PermissionDenied
        if not post_owner.is_public and user not in post_owner.get_followers and post_owner != user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.login_user = self.request.user.profile

        if '/show_likes/' in self.request.path:
            context['people'] = self.post.get_reactions()['likes']
            context['likes'] = True
        elif '/show_dislikes/' in self.request.path:
            context['people'] = self.post.get_reactions()['dislikes']
            context['dislikes'] = True

        return context
