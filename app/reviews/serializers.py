from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes_number')
    dislikes = serializers.SerializerMethodField('get_dislikes_number')

    class Meta:
        model = Review
        fields = ['id', 'user', 'title', 'content', 'movie', 'series', 'created', 'stars', 'likes', 'dislikes']

    def get_likes_number(self, obj):
        return obj.users_liked.filter(like=True).count()

    def get_dislikes_number(self, obj):
        return obj.users_liked.filter(like=False).count()


class ReviewSerializerForUpdate(ReviewSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'title', 'content', 'movie', 'series', 'created', 'stars', 'likes', 'dislikes']
        read_only_fields = ['movie', 'series']
