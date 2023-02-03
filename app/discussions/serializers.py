from django.core.paginator import Paginator
from rest_framework import serializers

from discussions.models import Discussion, Comment


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = ['id', 'title', 'content', 'created', 'updated', 'user', 'movie']


class DiscussionSerializerWithComments(serializers.ModelSerializer):
    comments_new = serializers.SerializerMethodField('paginated_comments')

    class Meta:
        model = Discussion
        fields = ['id', 'title', 'content', 'created', 'updated', 'user', 'movie', 'comments', 'comments_new']

    def paginated_comments(self, obj):
        page_size = self.context['request'].query_params.get('size') or 5
        page_number = self.context['request'].query_params.get('page') or 1
        paginator = Paginator(obj.comments.all(), page_size)
        data = paginator.page(page_number)
        serializer = CommentSerializer(data, many=True)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'discussion']
