from django.urls import path
from . import views

app_name = 'reactions'

urlpatterns = [
    path('like/post/<int:pk>', views.LikeView.as_view(), name='like'),
    path('dislike/post/<int:pk>', views.LikeView.as_view(), name='dislike'),
    path('follow/<int:pk>', views.FollowView.as_view(), name='follow_user'),
    path('unfollow/<int:pk>', views.FollowView.as_view(), name='unfollow_user'),
    path('delete_comment/<int:pk>', views.DeleteComment.as_view(), name='delete_comment'),
    path('show_likes/<int:pk>', views.ShowLikes.as_view(), name='show_likes'),
    path('show_dislikes/<int:pk>', views.ShowLikes.as_view(), name='show_dislikes'),
]
