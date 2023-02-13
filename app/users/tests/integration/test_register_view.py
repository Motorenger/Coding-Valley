import pytest
from django.urls import reverse
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from users.models import User


pytestmark = pytest.mark.django_db


class TestRegisterView:
    def test_post_with_correct_data(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": "user_email@email.com",
            "password": "user_password",
            "password2": "user_password"
        }
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 201, "Status code of response must be 201"
        assert response.json().get("first_name") == user_registration_data["first_name"], f"The response must contain {user_registration_data['first_name']} for 'first_name' field"
        assert response.json().get("last_name") == user_registration_data["last_name"], f"The response must contain {user_registration_data['last_name']} for 'last_name' field"
        assert response.json().get("email") == user_registration_data["email"], f"The response must contain {user_registration_data['email']} for 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is not None, "The response must contain access token"
        assert response.json().get("refresh") is not None, "The response must contain refresh token"
        assert User.objects.count() == 1, "The db must contain one user"
        assert OutstandingToken.objects.count() == 2, "The db must contain 2 outstanding tokens"

    def test_post_without_data(self, api_client):
        # given
        user_registration_data = {}
        expected_error_message = ["This field is required."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") == expected_error_message, f"The response must contain {expected_error_message} for 'first_name' field"
        assert response.json().get("last_name") == expected_error_message, f"The response must contain {expected_error_message} for 'last_name' field"
        assert response.json().get("email") == expected_error_message, f"The response must contain {expected_error_message} for 'email' field"
        assert response.json().get("password") == expected_error_message, f"The response must contain {expected_error_message} for 'password' field"
        assert response.json().get("password2") == expected_error_message, f"The response must contain {expected_error_message} for 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_existent_email(self, api_client, registered_user):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": registered_user.email,
            "password": "user_password",
            "password2": "user_password"
        }
        expected_error_message = ["This field must be unique."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") == expected_error_message, f"The response must contain {expected_error_message} for 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 1, "The db must contain one user"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_incorrect_email(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": "user_email",
            "password": "user_password",
            "password2": "user_password"
        }
        expected_error_message = ["Enter a valid email address."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") == expected_error_message, f"The response must contain {expected_error_message} for 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_incorrect_passwords(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": "user_email@email.com",
            "password": "p",
            "password2": "p"
        }
        expected_error_message = [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common."
        ]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") == expected_error_message, f"The response must contain {expected_error_message} for 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_different_passwords(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name",
            "email": "user_email@email.com",
            "password": "user_password",
            "password2": "another_user_password"
        }
        expected_error_message = ["Password fields didn't match."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") == expected_error_message, f"The response must contain {expected_error_message} for 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_incorrect_first_name(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name222",
            "last_name": "user_last_name",
            "email": "user_email@email.com",
            "password": "user_password",
            "password2": "user_password"
        }
        expected_error_message = ["First name can only contain alphabet letters."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") == expected_error_message, f"The response must contain {expected_error_message} for 'first_name' field"
        assert response.json().get("last_name") is None, "The response must not contain 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_post_with_incorrect_last_name(self, api_client):
        # given
        user_registration_data = {
            "first_name": "user_first_name",
            "last_name": "user_last_name222",
            "email": "user_email@email.com",
            "password": "user_password",
            "password2": "user_password"
        }
        expected_error_message = ["Last name can only contain alphabet letters."]
        # when
        response = api_client.post(reverse("users_app:register"), user_registration_data)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("first_name") is None, "The response must not contain 'first_name' field"
        assert response.json().get("last_name") == expected_error_message, f"The response must contain {expected_error_message} for 'last_name' field"
        assert response.json().get("email") is None, "The response must not contain 'email' field"
        assert response.json().get("password") is None, "The response must not contain 'password' field"
        assert response.json().get("password2") is None, "The response must not contain 'password2' field"
        assert response.json().get("access") is None, "The response must not contain access token"
        assert response.json().get("refresh") is None, "The response must not contain refresh token"
        assert User.objects.count() == 0, "The db must contain no users"
        assert OutstandingToken.objects.count() == 0, "The db must contain no outstanding tokens"

    def test_get(self, api_client):
        # when
        response = api_client.get(reverse("users_app:register"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_put(self, api_client):
        # when
        response = api_client.put(reverse("users_app:register"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_patch(self, api_client):
        # when
        response = api_client.patch(reverse("users_app:register"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_delete(self, api_client):
        # when
        response = api_client.delete(reverse("users_app:register"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"
