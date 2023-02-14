from django.contrib import admin

from users.models import User, UserProfile


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("username", "email", "get_full_name",)
    search_fields = ("username",)
    list_filter = ("is_superuser", "is_staff")
    list_per_page = 10


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ("user", "get_followers")
    search_fields = ("user",)
    list_per_page = 10
