from django.contrib import admin

from users.models import User, UserProfile


@admin.register(User)
class User(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    list_per_page = 10


@admin.register(UserProfile)
class UserProfile(admin.ModelAdmin):
    list_display = ("user",)
    list_per_page = 10
