from django.contrib import admin

from discussions.models import Discussion, Comment


class CommentInline(admin.TabularInline):
    model = Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "discussion", "created")
    list_filter = ("discussion",)
    search_fields = ("user", "discussion")
    fields = ("user", "discussion", "content")


@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ("title", "updated", "user", "media")
    list_filter = ("user", "media")
    search_fields = ("user", "media")
    fields = ("title", "content", "user", "media")
    inlines = [
        CommentInline,
    ]
