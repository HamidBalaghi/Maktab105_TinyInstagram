from django.contrib import admin
from .models import Like, Comment


# Register your models here.

class LikeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'liked', 'disliked')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'parent_comment', 'is_deleted')


admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
