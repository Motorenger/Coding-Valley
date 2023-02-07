from django.contrib import admin

from notifications.models import Notification


@admin.register(Notification)
class Notification(admin.ModelAdmin):
    list_per_page = 10
