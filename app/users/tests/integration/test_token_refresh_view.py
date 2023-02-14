import pytest

from django.urls import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken
)


pytestmark = pytest.mark.django_db


class TestTokenRefreshView:
    def test_post_with_correct_refresh_token(self, api_client, registered_user):
        # given
        refresh_token = RefreshToken.for_user(registered_user)
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse('users_app:token_refresh'), {'refresh': str(refresh_token)})
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('access') is not None, 'The response must contain access token'
        assert response.json().get('refresh') is not None, 'The response must contain refresh token'
        assert response.json().get('refresh') != refresh_token, 'The refresh token in response and the given refresh_token must be different'
        assert BlacklistedToken.objects.count() == 1, 'The db must contain one blacklisted token'
        assert BlacklistedToken.objects.first().token.token == str(refresh_token), 'The blacklisted token must be equal to the given refresh_token'

    def test_post_without_refresh_token(self, api_client, registered_user):
        # given
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse('users_app:token_refresh'))
        # then
        assert response.status_code == 400, 'Status code of response must be 400'
        assert response.json().get('refresh') == ['This field is required.'], 'The response must contain "This field is required."" for "refresh" field'
        assert response.json().get('access') is None, 'The response must not contain access token'
        assert BlacklistedToken.objects.count() == 0, 'The db must contain no blacklisted tokens'

    def test_post_with_incorrect_refresh_token(self, api_client, registered_user):
        # given
        incorrect_refresh_token = 'incorrect_refresh_token'
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse('users_app:token_refresh'), {'refresh': incorrect_refresh_token})
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert response.json().get('detail') == 'Token is invalid or expired', 'The response must contain "Token is invalid or expired" for "detail" field'
        assert response.json().get('code') == 'token_not_valid', 'The response must contain "token_not_valid" for "code" field'
        assert response.json().get('access') is None, 'The response must not contain access token'
        assert response.json().get('refresh') is None, 'The response must not contain refresh token'
        assert BlacklistedToken.objects.count() == 0, 'The db must contain no blacklisted tokens'

    def test_post_with_blacklisted_refresh_token(self, api_client, registered_user):
        # given
        refresh_token = RefreshToken.for_user(registered_user)
        refresh_token.blacklist()
        api_client.force_authenticate(user=registered_user)
        # when
        response = api_client.post(reverse('users_app:token_refresh'), {'refresh': str(refresh_token)})
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert response.json().get('detail') == 'Token is blacklisted', 'The response must contain "Token is blacklisted" for "detail" field'
        assert response.json().get('code') == 'token_not_valid', 'The response must contain "token_not_valid" for "code" field'
        assert response.json().get('access') is None, 'The response must not contain access token'
        assert response.json().get('refresh') is None, 'The response must not contain refresh token'
        assert BlacklistedToken.objects.count() == 1, 'The db must contain one blacklisted token'
        assert BlacklistedToken.objects.first().token.token == str(refresh_token), 'The blacklisted token must be equal to the given refresh_token'

    def test_post_with_unauthenticated_user(self, api_client, registered_user):
        # given
        refresh_token = RefreshToken.for_user(registered_user)
        # when
        response = api_client.post(reverse('users_app:token_refresh'), {'refresh': str(refresh_token)})
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('access') is not None, 'The response must contain access token'
        assert response.json().get('refresh') is not None, 'The response must contain refresh token'
        assert response.json().get('refresh') != refresh_token, 'The refresh token in response and the given refresh_token must be different'
        assert BlacklistedToken.objects.count() == 1, 'The db must contain one blacklisted token'
        assert BlacklistedToken.objects.first().token.token == str(refresh_token), 'The blacklisted token must be equal to the given refresh_token'

    def test_get(self, api_client):
        # when
        response = api_client.get(reverse('users_app:token_refresh'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_put(self, api_client):
        # when
        response = api_client.put(reverse('users_app:token_refresh'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_patch(self, api_client):
        # when
        response = api_client.patch(reverse('users_app:token_refresh'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_delete(self, api_client):
        # when
        response = api_client.delete(reverse('users_app:token_refresh'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'
