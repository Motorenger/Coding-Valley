from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'mobile',
            'bio', 'password', 'is_superuser', 'is_staff'
        )
        read_only_fields = ("is_superuser", "is_staff")
