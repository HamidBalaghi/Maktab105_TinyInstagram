from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, DetailView, ListView
from .forms import NewPostForm
from accounts.models import Profile
from .models import Post, Image
from core.mixin import LoginRequiredMixin, NavbarMixin
from reactions.forms import NewCommentForm
from reactions.models import Comment


class NewPostView(LoginRequiredMixin, NavbarMixin, FormView):
    form_class = NewPostForm
    template_name = 'post/newpost.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs['pk']
        self.owner = get_object_or_404(Profile, pk=self.pk)
        if request.user.is_authenticated and self.owner != request.user.profile:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.pk})

    def form_valid(self, form):
        description = form.cleaned_data['description']
        images = [form.cleaned_data[f'image{i}'] for i in range(1, 5)]

        new_post = Post.objects.create(profile=self.owner, description=description)
        for image in images:
            if image:
                Image.objects.create(post=new_post, image=image)

        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, NavbarMixin, DetailView):
    model = Post
    template_name = 'post/postdetail.html'
    context_object_name = 'post'

    def dispatch(self, request, *args, **kwargs):
        self.owner = self.get_object().profile
        if isinstance(request.user, AnonymousUser):
            return redirect('accounts:login')
        elif (not self.get_object().publishable
              or (request.user.profile != self.owner
                  and not self.get_object().is_active)
              or not self.owner.is_active):
            raise PermissionDenied
        elif (request.user.profile not in self.owner.get_followers
              and not self.owner.is_public
              and request.user.profile != self.owner):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comment_form'] = NewCommentForm()
        context['comments'] = post.get_comments()
        context['reactions'] = post.get_reactions()
        context['post_owner'] = self.owner
        context['user'] = self.request.user.profile
        like_reaction = post.user_reaction(self.request.user.profile)
        context[like_reaction] = True
        return context

    def post(self, request, *args, **kwargs):
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            parent_id = comment_form.cleaned_data['parent']

            ## new comment
            new_comment = Comment(profile=request.user.profile, post=self.get_object(), comment=text)
            if parent_id == 'None':
                ## new comment without reply
                new_comment.save()
            else:
                ## new comment with reply
                parent = Comment.objects.get(pk=parent_id)
                new_comment.parent_comment = parent
                new_comment.save()

        else:
            print('invalid (test)')

        return redirect('post:post', pk=self.kwargs['pk'])


class HomeView(LoginRequiredMixin, NavbarMixin, ListView):
    model = Post
    template_name = 'home/home.html'

    def get_queryset(self):
        queryset = super().get_queryset()

        user = self.request.user.profile
        following = user.get_followings

        queryset = queryset.filter(profile__in=following)
        queryset = queryset.order_by('-publish_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.profile
        posts = self.get_queryset()
        context['postss'] = posts
        for post in posts:
            post.user_like_reaction = post.user_reaction(user)

        return context


class ExploreView(LoginRequiredMixin, NavbarMixin, ListView):
    model = Post
    template_name = 'profile/explore.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        user_following = self.request.user.profile.get_followings
        queryset = queryset.filter(is_active=True, publishable=True, profile__is_public=True).exclude(
            profile__in=user_following)
        queryset = queryset.order_by('-publish_at')

        return queryset


class SuggestView(LoginRequiredMixin, NavbarMixin, ListView):
    model = Profile
    template_name = 'profile/follow.html'
    context_object_name = 'people'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.user_following = self.request.user.profile.get_followings
        following = [profile.pk for profile in self.user_following]
        user_pk = self.request.user.profile.pk
        queryset = queryset.filter(is_active=True, is_public=True).exclude(pk__in=following + [user_pk])
        queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.profile
        context['user_following'] = self.user_following
        context['suggest'] = True
        return context
