import pytest
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken
)


pytestmark = pytest.mark.django_db


class TestLoginView:
    def test_post_with_correct_data(self, api_client, registered_user):
        # given
        user_authentication_data = {
            "email": "user_email@email.com",
            "password": "user_password"
        }
        # when
        response = api_client.post(reverse("users_app:login"), user_authentication_data)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get("id") == str(registered_user.id), f"The response must contain {registered_user.id} for 'id' field"
        assert response.json().get("first_name") == registered_user.first_name, f"The response must contain {registered_user.first_name} for 'first_name' field"
        assert response.json().get("last_name") == registered_user.last_name, f"The response must contain {registered_user.last_name} for 'last_name' field"
        assert response.json().get("email") == registered_user.email, f"The response must contain {registered_user.email} for 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("access") is not None, "The response must contain access token"
        assert response.json().get("refresh") is not None, "The response must contain refresh token"
        assert OutstandingToken.objects.count() == 3, "The db must contain 3 outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_without_data(self, api_client, registered_user):
        # given
        user_authentication_data = {}
        expected_error_message = ["This field is required."]
        # when
        response = api_client.post(reverse("users_app:login"), user_authentication_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("id") is None, "The response must not contain 'id' field"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") == expected_error_message, f"The response must contain {expected_error_message} for 'email' field"
        assert response.json().get("password") == expected_error_message, f"The response must contain {expected_error_message} for 'password' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_with_nonexistent_email(self, api_client, registered_user):
        # given
        user_authentication_data = {
            "email": "nonexistent_user_email@email.com",
            "password": "user_password"
        }
        expected_error_message = "No active account found with the given credentials"
        # when
        response = api_client.post(reverse("users_app:login"), user_authentication_data)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get("detail") == expected_error_message, f"The response must contain {expected_error_message} for 'detail' field"
        assert response.json().get("id") is None, "The response must not contain 'id' field"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_post_with_incorrect_password(self, api_client, registered_user):
        # given
        user_authentication_data = {
            "email": "user_email@email.com",
            "password": "incorrect_user_password"
        }
        expected_error_message = "No active account found with the given credentials"
        # when
        response = api_client.post(reverse("users_app:login"), user_authentication_data)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get("detail") == expected_error_message, f"The response must contain {expected_error_message} for 'detail' field"
        assert response.json().get("id") is None, "The response must not contain 'id' field"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"
        assert BlacklistedToken.objects.count() == 0, "The db must contain no blacklisted tokens"

    def test_get(self, api_client):
        # when
        response = api_client.get(reverse("users_app:login"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_put(self, api_client):
        # when
        response = api_client.put(reverse("users_app:login"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_patch(self, api_client):
        # when
        response = api_client.patch(reverse("users_app:login"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_delete(self, api_client):
        # when
        response = api_client.delete(reverse("users_app:login"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"
