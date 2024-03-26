from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, UpdateView, DetailView
from .forms import CustomSignUpForm, CustomUserLoginForm, VerifyForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User
from django.utils import timezone
from datetime import timedelta
from .utils import otp_sender
from .models import Profile


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'

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
                if (timezone.now() - user.otp_created_at) > timedelta(minutes=5):
                    otp_sender(user)
                return redirect('accounts:activation', pk=user.pk)  ## todo : i will redirect user to profile
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

    def form_valid(self, form):
        self.pk = self.kwargs['pk']
        self.new_user = User.objects.get(pk=self.pk)
        code = form.cleaned_data.get('code')
        if code == str(self.new_user.otp) and (timezone.now() - self.new_user.otp_created_at) < timedelta(minutes=5):
            if not self.new_user.is_active:
                self.new_user.is_active = True
                self.new_user.save()
                Profile.objects.create(user=self.new_user)  # Attribution a profile to new user
            login(self.request, self.new_user)
            return redirect('accounts:login')  ## todo : i will redirect user to profile
        else:
            form.add_error(None, 'Invalid code or OTP expired.')
            return self.form_invalid(form)


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'account/editprofile.html'
    fields = ['image', 'about_me']
    success_url = reverse_lazy('accounts:test')


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile/profile.html'
    context_object_name = 'profile'


def test(request, *args, **kwargs):
    return render(request, template_name='test/test.html')
