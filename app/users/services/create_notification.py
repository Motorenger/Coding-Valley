from notifications.models import Notification


def create_notification(user_to_follow, user):
    return Notification.objects.create(
        to_user=user_to_follow,
        created_by=user,
        notification_type='follow',
        followed_by=user,
        content=f"{user.userprofile.user} started following you."
    )
