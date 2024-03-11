from django.contrib import admin
from .models import User, Profile, Follow


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_active', 'is_admin')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'is_active', 'is_public')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('profile', 'following', 'accepted')


admin.site.register(User, UserAccountAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)
