from rest_framework import serializers

from discussions.models import Discussion, Comment


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'content', 'created', 'updated', 'user', 'movie']
        read_only_fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'discussion']
        read_only_fields = ['id']
