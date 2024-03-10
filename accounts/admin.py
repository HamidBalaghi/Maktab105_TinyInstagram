from django.contrib import admin
from .models import User


class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'is_active', 'is_admin')


admin.site.register(User, UserAccountAdmin)
