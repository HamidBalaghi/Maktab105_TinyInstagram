from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import NewPostForm
from accounts.models import Profile
from .models import Post, Image


class NewPostView(FormView):
    form_class = NewPostForm
    template_name = 'post/newpost.html'

    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs['pk']
        self.owner = get_object_or_404(Profile, pk=self.pk)
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
