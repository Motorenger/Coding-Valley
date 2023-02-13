import pytest
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken
)

from users.models import User


pytestmark = pytest.mark.django_db


class TestLogoutAllView:
    def test_post_with_tokens_for_registered_user(self, api_client, registered_user):
        # given
        [RefreshToken.for_user(registered_user) for _ in range(5)]
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 205, "Status code of response must be 205"
        assert OutstandingToken.objects.count() == 5, "The db must contain 5 outstanding tokens"
        assert BlacklistedToken.objects.count() == 5, "The db must contain 5 blacklisted tokens"

    def test_post_with_tokens_for_another_user(self, api_client, registered_user):
        # given
        another_user = User.objects.create(
            first_name="another_user_first_name",
            last_name="another_user_last_name",
            email="another_user_email@email.com",
            password=make_password("another_user_password")
        )
        [RefreshToken.for_user(registered_user) for _ in range(5)]
        api_client.force_authenticate(user=another_user)
        # when
        response = api_client.post(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 205, "Status code of response must be 205"
        assert OutstandingToken.objects.count() == 5, "The db must contain 5 outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_with_unauthenticated_user(self, api_client, registered_user):
        # when
        [RefreshToken.for_user(registered_user) for _ in range(5)]
        response = api_client.post(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 401, "Status code of response must be 491"
        assert OutstandingToken.objects.count() == 5, "The db must contain 5 outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_get_with_unauthenticated_user(self, api_client):
        # when
        response = api_client.get(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 401, "Status code of response must be 401"

    def test_get_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.get(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_put_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_patch_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.patch(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_delete_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.delete(reverse("users_app:logout_all"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"
