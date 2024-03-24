from django.views.generic import CreateView, FormView
from .forms import CustomSignUpForm, CustomUserLoginForm, VerifyForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import User


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.save()
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
                login(request, user)
                return redirect('accounts:signup')  # Redirect to the desired page after login
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
        self.new_user = User.objects.get(pk=self.pk)
        if self.new_user.is_active:
            return redirect('accounts:login')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        code = form.cleaned_data.get('code')
        if code == str(self.new_user.otp):
            self.new_user.is_active = True
            self.new_user.save()
            login(self.request, self.new_user)
            return redirect('accounts:login')  ## todo : i will redirect user to profile
        else:
            form.add_error(None, 'Invalid code')
            return self.form_invalid(form)
