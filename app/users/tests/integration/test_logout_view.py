import pytest
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken
)

pytestmark = pytest.mark.django_db


class TestLogoutView:
    def test_post_with_correct_refresh_token(self, api_client, registered_user):
        # given
        refresh_token = RefreshToken.for_user(registered_user)
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse("users_app:logout"), {"refresh_token": str(refresh_token)})
        # then
        assert response.status_code == 205, "Status code of response must be 205"
        assert OutstandingToken.objects.count() == 1, "The db must contain one outstanding token"
        assert BlacklistedToken.objects.count() == 1, "The db must contain one blacklisted token"
        assert BlacklistedToken.objects.first().token.token == str(refresh_token), "The blacklisted token must be equal to the given refresh_token"

    def test_post_without_refresh_token(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse("users_app:logout"))
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_with_incorrect_refresh_token(self, api_client, registered_user):
        # given
        incorrect_refresh_token = "incorrect_refresh_token"
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse("users_app:logout"), {"refresh_token": incorrect_refresh_token})
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_with_unauthenticated_user(self, api_client, registered_user):
        # when
        refresh_token = RefreshToken.for_user(registered_user)
        response = api_client.post(reverse("users_app:logout"), {"refresh_token": str(refresh_token)})
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert OutstandingToken.objects.count() == 1, "The db must contain one outstanding token"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_get_with_unauthenticated_user(self, api_client):
        # when
        response = api_client.get(reverse("users_app:logout"))
        # then
        assert response.status_code == 401, "Status code of response must be 401"

    def test_get_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.get(reverse("users_app:logout"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_put_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:logout"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_patch_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.patch(reverse("users_app:logout"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_delete_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.delete(reverse("users_app:logout"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"
