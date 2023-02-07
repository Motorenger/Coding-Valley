from django.core.paginator import Paginator
from django.urls import reverse
from rest_framework import serializers

from discussions.models import Discussion, Comment


class DiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discussion
        fields = [
            'id', 'title', 'content', 'created',
            'updated', 'user', 'media'
        ]


class DiscussionSerializerWithComments(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField('get_paginated_comments')

    class Meta:
        model = Discussion
        fields = [
            'id', 'title', 'content', 'created',
            'updated', 'user', 'media', 'comments'
        ]

    def get_paginated_comments(self, obj):
        page_size = self.context['request'].query_params.get('size', 5)
        page_number = self.context['request'].query_params.get('page', 1)
        url = reverse('discussions_app:discussions-detail', args=(obj.id,))
        paginator = Paginator(obj.comments.all(), page_size)
        page = self.get_page(paginator, page_number, page_size, url)
        return page

    def get_page(self, paginator, page_number, page_size, url):
        page_obj = paginator.page(page_number)
        page = {
            "count": paginator.count,
            "next": self.get_next_link(url, page_size, page_obj),
            "previous": self.get_previous_link(url, page_size, page_obj),
            "results": CommentSerializer(page_obj, many=True).data
        }
        return page

    @staticmethod
    def get_next_link(url, page_size, page_obj):
        if page_obj.has_next():
            return f"{url}?size={page_size}&page={page_obj.next_page_number()}"
        return None

    @staticmethod
    def get_previous_link(url, page_size, page_obj):
        if page_obj.has_previous():
            return f"{url}?size={page_size}&page={page_obj.previous_page_number()}"
        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'discussion']


class CommentSerializerForUpdate(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content']
