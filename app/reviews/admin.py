from django.contrib import admin

from reviews.models import Review, ReviewLikes


class ReviewLikesInline(admin.TabularInline):
    model = ReviewLikes


class ReviewAdmin(admin.ModelAdmin):
    inlines = [
        ReviewLikesInline,
    ]


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewLikes)
