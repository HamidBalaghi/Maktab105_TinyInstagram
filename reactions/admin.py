from django.contrib import admin
from .models import Like, Comment, Hashtag


# Register your models here.

class LikeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'liked', 'disliked')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'post', 'parent_comment', 'is_deleted')


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)
