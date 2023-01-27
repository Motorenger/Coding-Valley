from django.contrib import admin

from reviews.models import Review, ReviewLikes


admin.site.register(Review)
admin.site.register(ReviewLikes)
