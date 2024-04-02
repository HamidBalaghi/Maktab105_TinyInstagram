from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'post'

urlpatterns = [
    path('newpost/<int:pk>', views.NewPostView.as_view(), name='create_post'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post'),
    path('', views.HomeView.as_view(), name='home'),

]
