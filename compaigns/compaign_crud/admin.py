from django.contrib import admin
from .models import Compaign, UrlEmail


@admin.register(Compaign)
class CompaignAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'description', 'user']
    list_display_links = ['id', 'title']
    list_filter = ['id', 'user']
    search_fields = ['id', 'user']


@admin.register(UrlEmail)
class UrlEmailAdmin(admin.ModelAdmin):

    list_display = ['id', 'url', 'email', 'user']
    list_display_links = ['id', 'url']
    list_filter = ['id', 'user']
    search_fields = ['id', 'user']
    list_per_page = 10
