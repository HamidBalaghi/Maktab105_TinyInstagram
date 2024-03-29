from django.contrib import admin
from .models import Post, Image


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('profile', 'publish_at', 'is_active', 'publishable')
    ordering = ('-publish_at',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('post',)


admin.site.register(Post, PostAdmin)
admin.site.register(Image, ImageAdmin)
