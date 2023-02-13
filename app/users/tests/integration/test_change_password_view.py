import pytest
from django.contrib.auth.hashers import check_password
from django.urls import reverse


pytestmark = pytest.mark.django_db


class TestChangePasswordView:
    def test_put_with_correct_data(self, api_client, registered_user):
        # given
        old_password = "user_password"
        new_password = "new_user_password"
        user_data_for_changing_password = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": new_password
        }
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert not check_password(old_password, registered_user.password), "The currect user password must not be equal to the old password"
        assert check_password(new_password, registered_user.password), "The currect user password must be equal to the new password"

    def test_put_without_data(self, api_client, registered_user):
        # given
        old_password = "user_password"
        user_data_for_changing_password = {}
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert check_password(old_password, registered_user.password), "The currect user password must be equal to the old password"

    def test_put_with_incorrect_new_passwords(self, api_client, registered_user):
        # given
        old_password = "user_password"
        incorrect_new_password = "p"
        user_data_for_changing_password = {
            "old_password": old_password,
            "new_password": incorrect_new_password,
            "confirm_password": incorrect_new_password
        }
        expected_error_message = [
            "This password is too short. It must contain at least 8 characters.",
            "This password is too common."
        ]
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("new_password") == expected_error_message, f"The response must contain {expected_error_message} for 'new_password' field"
        assert check_password(old_password, registered_user.password), "The currect user password must be equal to the old password"
        assert not check_password(incorrect_new_password, registered_user.password), "The currect user password must not be equal to the new password"

    def test_put_with_incorrect_old_password(self, api_client, registered_user):
        # given
        old_password = "user_password"
        incorrect_old_password = "incorrect_user_password"
        new_password = "new_user_password"
        user_data_for_changing_password = {
            "old_password": incorrect_old_password,
            "new_password": new_password,
            "confirm_password": new_password
        }
        expected_error_message = {
            "old_password": "Old password is not correct"
        }
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("old_password") == expected_error_message, f"The response must contain {expected_error_message} for 'old_password' field"
        assert check_password(old_password, registered_user.password), "The currect user password must be equal to the old password"
        assert not check_password(new_password, registered_user.password), "The currect user password must not be equal to the new password"

    def test_put_with_different_new_passwords(self, api_client, registered_user):
        # given
        old_password = "user_password"
        new_password = "new_user_password"
        another_new_password = "another_new_user_password"
        user_data_for_changing_password = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": another_new_password
        }
        expected_error_message = ["Password fields didn't match."]
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 400, "Status code of response must be 400"
        assert response.json().get("password") == expected_error_message, f"The response must contain {expected_error_message} for 'password' field"
        assert check_password(old_password, registered_user.password), "The currect user password must be equal to the old password"
        assert not check_password(new_password, registered_user.password), "The currect user password must not be equal to the new password"
        assert not check_password(another_new_password, registered_user.password), "The currect user password must not be equal to the another new password"

    def test_put_with_unauthenticated_user(self, api_client, registered_user):
        # given
        old_password = "user_password"
        new_password = "new_user_password"
        user_data_for_changing_password = {
            "old_password": old_password,
            "new_password": new_password,
            "confirm_password": new_password
        }
        # when
        response = api_client.put(reverse("users_app:auth_change_password"), user_data_for_changing_password)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert check_password(old_password, registered_user.password), "The currect user password must be equal to the old password"
        assert not check_password(new_password, registered_user.password), "The currect user password must not be equal to the new password"

    def test_get_with_unauthenticated_user(self, api_client):
        # when
        response = api_client.get(reverse("users_app:auth_change_password"))
        # then
        assert response.status_code == 401, "Status code of response must be 401"

    def test_get_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.get(reverse("users_app:auth_change_password"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_post_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse("users_app:auth_change_password"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_delete_with_authenticated_user(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.delete(reverse("users_app:auth_change_password"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"
