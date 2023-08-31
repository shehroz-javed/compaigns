from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['id', 'username', 'email', 'is_active']
    list_editable = ['is_active']
    list_display_links = ['id', 'username']
    list_filter = ['username', 'is_active']
    search_fields = ['username', 'is_active']
