from rest_framework import serializers

from ..models import Discussion


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'content', 'created', 'updated', 'user', 'movie']
        read_only_fields = ['id']
