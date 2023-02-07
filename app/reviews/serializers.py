from rest_framework import serializers

from reviews.models import Review, ReviewLikes


class ReviewSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField('get_likes_number')
    dislikes = serializers.SerializerMethodField('get_dislikes_number')
    current_user_reviewlike = serializers.SerializerMethodField('get_current_user_reviewlike')

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'title', 'content', 'media',
            'created', 'stars', 'likes', 'dislikes',
            'current_user_reviewlike'
        ]

    def get_likes_number(self, obj):
        return obj.users_liked.filter(like=True).count()

    def get_dislikes_number(self, obj):
        return obj.users_liked.filter(like=False).count()

    def get_current_user_reviewlike(self, obj):
        current_user = self.context['request'].user
        if not current_user.is_authenticated:
            return None

        try:
            reviewlike = obj.users_liked.get(user=current_user)
        except ReviewLikes.DoesNotExist:
            return None
        return {'id': reviewlike.id, 'like': reviewlike.like}


class ReviewSerializerForUpdate(ReviewSerializer):
    class Meta:
        model = Review
        fields = ['title', 'content', 'stars']


class ReviewLikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLikes
        fields = ['id', 'review', 'user', 'like']
