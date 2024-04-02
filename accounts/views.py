# from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from core.mixin import LoginRequiredMixin, ProfilePermissionMixin, NavbarMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DetailView, TemplateView
from .forms import CustomSignUpForm, CustomUserLoginForm, VerifyForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.utils import timezone
from datetime import timedelta
from .utils import otp_sender
from .models import Profile


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'

    def dispatch(self, request, *args, **kwargs):
        time_limit = timezone.now() - timedelta(minutes=5)
        User.objects.filter(is_active=False, otp_created_at__lt=time_limit).delete()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        otp_sender(user)
        return redirect('accounts:activation', pk=user.pk)


class CustomUserLoginView(View):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                # if (timezone.now() - user.otp_created_at) > timedelta(minutes=5):
                #     otp_sender(user)
                # return redirect('accounts:activation', pk=user.pk)
                ##for test
                login(request, user)
                return redirect('accounts:profile', pk=user.pk)
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, self.template_name, {'form': form})


class CustomUserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')


class UserActivationView(FormView):
    template_name = 'account/verification.html'
    form_class = VerifyForm

    def dispatch(self, request, *args, **kwargs):
        self.pk = self.kwargs['pk']
        self.new_user = get_object_or_404(User, pk=self.pk)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data.get('code')
        if code == str(self.new_user.otp) and (timezone.now() - self.new_user.otp_created_at) < timedelta(minutes=5):
            if not self.new_user.is_active:
                self.new_user.is_active = True
                self.new_user.save()
                login(self.request, self.new_user)
                Profile.objects.create(user=self.new_user)  # Attribution a profile to new user
                return redirect('accounts:editprofile', pk=self.pk)
            login(self.request, self.new_user)
            return redirect('accounts:profile', pk=self.pk)
        else:
            form.add_error(None, 'Invalid code or OTP expired.')
            return self.form_invalid(form)


class EditProfileView(LoginRequiredMixin, NavbarMixin, UpdateView):
    model = Profile
    template_name = 'account/editprofile.html'
    fields = ['image', 'about_me', 'is_active', 'is_public']

    def dispatch(self, request, *args, **kwargs):
        if isinstance(request.user, AnonymousUser):
            return redirect('accounts:login')

        elif request.user.profile != self.get_object():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.kwargs['pk']})


class ProfileView(LoginRequiredMixin, ProfilePermissionMixin, NavbarMixin, DetailView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'


class ShowFollowView(LoginRequiredMixin, NavbarMixin, DetailView):
    model = Profile
    template_name = 'profile/follow.html'
    context_object_name = 'profile'

    def dispatch(self, request, *args, **kwargs):
        self.profile = get_object_or_404(Profile, user_id=self.kwargs.get('pk'))
        if not self.profile.is_active and self.profile != self.request.user:
            raise PermissionDenied
        elif isinstance(request.user, AnonymousUser):
            return redirect('accounts:login')
        elif request.user.profile != self.profile and request.user.profile not in self.profile.get_followers and not self.profile.is_public:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.login_user = self.request.user.profile

        if 'followers' in self.request.path:
            context['people'] = []
            temp = self.profile.get_followers
            for follower in temp:
                if follower.is_active:
                    context['people'].append(follower)
            context['followers'] = True
        elif 'following' in self.request.path:
            context['people'] = []
            temp = self.profile.get_followings
            for following in temp:
                if following.is_active:
                    context['people'].append(following)
        context['user_following'] = self.login_user.get_followings
        context['user'] = self.login_user
        return context


def test(request, *args, **kwargs):
    return render(request, template_name='test/test.html')
