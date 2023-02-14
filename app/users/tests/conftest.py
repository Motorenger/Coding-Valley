import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def registered_user():
    user = User.objects.create(
        first_name='user_first_name',
        last_name='user_last_name',
        email='user_email@email.com',
        password=make_password('user_password')
    )
    return user
