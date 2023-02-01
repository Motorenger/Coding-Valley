import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    user = get_user_model().objects.create(
        email="test_user@email.com",
        username="test_user_name",
        password="test_user_password"
    )
    return user


@pytest.fixture
def owner():
    owner = get_user_model().objects.create(
        email="test_owner@email.com",
        username="test_owner_name",
        password="test_owner_password"
    )
    return owner


@pytest.fixture
def not_owner():
    not_owner = get_user_model().objects.create(
        email="test_not_owner@email.com",
        username="test_not_owner_name",
        password="test_not_owner_password"
    )
    return not_owner


@pytest.fixture
def admin():
    admin = get_user_model().objects.create(
        email="test_admin@email.com",
        username="test_admin_name",
        password="test_admin_password",
        is_staff=True,
        is_superuser=True
    )
    admin.save()
    return admin
