from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from accounts.models import Profile


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser) or not request.user.is_authenticated:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)


class ProfilePermissionMixin:
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if self.model.__name__ == 'Profile':
            owner = Profile.objects.get(user__id=pk)
            owner_followers = owner.get_followers
            owner_followings = owner.get_followings
            user = self.request.user.profile
            if not owner.is_active and user != owner:
                raise PermissionDenied
            if user == owner:
                context['owner'] = True
            elif owner in user.get_followings:
                context['is_following'] = True

            followers_temp = []
            for follower in owner_followers:
                if follower.is_active:
                    followers_temp.append(follower)
            context['followers_count'] = len(followers_temp)
            followings_temp = []
            for following in owner_followings:
                if following.is_active:
                    followings_temp.append(following)
            context['followings_count'] = len(followings_temp)

            if owner.is_public or user in owner_followers:
                context['posts'] = owner.posts.filter(publishable=True, is_active=True)
                context['has_perm'] = True
            elif user == owner:
                context['posts'] = owner.posts.filter(publishable=True)
                context['has_perm'] = True
        return context


class NavbarMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.profile
        context['logged_in_user'] = user
        context['logged_in_user_pk'] = user.pk
        context['logged_in_user_image'] = user.get_image_url
        return context
