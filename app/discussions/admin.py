from django.contrib import admin

from discussions.models import Discussion, Comment

admin.site.register(Discussion)
admin.site.register(Comment)
