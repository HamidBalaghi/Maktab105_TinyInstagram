from django.urls import path
from . import views

app_name = 'reactions'

urlpatterns = [
    path('like/post/<int:pk>', views.LikeView.as_view(), name='like'),
    path('dislike/post/<int:pk>', views.LikeView.as_view(), name='dislike'),
    path('follow/<int:pk>', views.FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:pk>', views.FollowView.as_view(), name='unfollow_user'),
]
