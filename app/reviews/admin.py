from django.contrib import admin

from reviews.models import Review, ReviewLikes


class ReviewLikesInline(admin.TabularInline):
    model = Review.likes.through


# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
#     list_display = ("user", "discussion", "created")
#     list_filter = ("discussion",)
#     search_fields = ("user", "discussion")
#     fields = ("user", "discussion", "content")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "media", "stars", "created", "get_likes")
    list_filter = ("stars", "media")
    fields = ("user", "title", "content", "stars", "media")
    inlines = [
        ReviewLikesInline,
    ]
