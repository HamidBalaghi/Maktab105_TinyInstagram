from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomSignUpForm, CustomUserLoginForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomSignUpForm
    success_url = reverse_lazy('accounts:login')  # Redirect to login page upon successful signup
    template_name = 'account/signup.html'


class CustomUserLoginView(View):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            print(email)
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(request, email=email, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('accounts:signup')  # Redirect to the desired page after login
            else:
                form.add_error(None, 'Invalid email or password')
        return render(request, self.template_name, {'form': form})


class CustomUserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        # Redirect to the desired page after logout
        return redirect('accounts:login')
