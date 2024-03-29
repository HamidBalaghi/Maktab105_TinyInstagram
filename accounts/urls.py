from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomUserLoginView.as_view(), name='login'),
    path('logout/', views.CustomUserLogoutView.as_view(), name='logout'),
    path('activation/<int:pk>', views.UserActivationView.as_view(), name='activation'),
    path('editprofile/<int:pk>', views.EditProfileView.as_view(), name='editprofile'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('followers/<int:pk>', views.ShowFollowView.as_view(), name='followers'),
    path('following/<int:pk>', views.ShowFollowView.as_view(), name='following'),

]
