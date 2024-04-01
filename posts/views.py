from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, DetailView
from .forms import NewPostForm
from accounts.models import Profile
from .models import Post, Image
from core.mixin import LoginRequiredMixin
from reactions.forms import NewCommentForm
from reactions.models import Comment


class NewPostView(LoginRequiredMixin, FormView):
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


class PostDetailView(LoginRequiredMixin, DetailView):
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
        like_reaction = post.user_reaction(self.request.user.profile)
        context[like_reaction] = True
        return context

    def post(self, request, *args, **kwargs):
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():
            text = comment_form.cleaned_data['text']
            parent_id = comment_form.cleaned_data['parent']

            new_comment = Comment(profile=request.user.profile, post=self.get_object(), comment=text)
            if parent_id == 'None':
                new_comment.save()

        else:
            print('invalid (test)')

        return redirect('post:post', pk=self.kwargs['pk'])
