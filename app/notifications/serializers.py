from rest_framework import serializers

from users.serializers import UserProfileSerializer
from reviews.serializers import ReviewSerializer
from notifications.models import Notification
from discussions.serializers import DiscussionSerializer


class NotificationSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField(read_only=True)
    followed_by = serializers.SerializerMethodField(read_only=True)
    review = serializers.SerializerMethodField(read_only=True)
    discussion = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

    def get_created_by(self, obj):
        return UserProfileSerializer(obj.created_by.userprofile, many=False).data

    def get_followed_by(self, obj):
        if obj.notification_type == 'follow':
            return UserProfileSerializer(obj.followed_by.userprofile, many=False).data
        return None

    def get_review(self, obj):
        if obj.notification_type == 'review':
            return ReviewSerializer(obj.review, many=False).data
        return None

    def get_discussion(self, obj):
        if obj.notification_type == 'discussion':
            return DiscussionSerializer(obj.discussion, many=False).data
        return None
