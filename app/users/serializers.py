from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'bio', 'is_active', 'is_staff', 'is_superuser'
        )
        read_only_fields = ('is_active' ,'is_superuser', 'is_staff')
