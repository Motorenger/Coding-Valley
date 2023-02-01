import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from model_bakery import baker


@pytest.mark.django_db
class TestDiscussionViewSet:
    # LIST
    def test_list_with_unauthenticated_user_with_no_discussions(self, api_client):
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 0, "The response must contain no discussions"

    def test_list_with_unauthenticated_user(self, api_client):
        # GIVEN
        baker.make("discussions.Discussion")
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 1, "The response must contain one discussion"

    def test_list_with_authenticated_user(self, api_client, user):
        # GIVEN
        baker.make("discussions.Discussion")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert len(response.json()) == 1, "The response must contain one discussion"

    # RETRIEVE
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # GIVEN
        discussion = baker.make("discussions.Discussion")
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('id') == str(discussion.id),  "The response must contain id of the given discussion"

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # GIVEN
        discussion = baker.make("discussions.Discussion")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('id') == str(discussion.id),  "The response must contain id of the given discussion"

    # CREATE
    def test_create_with_unauthenticated_user(self, api_client):
        # GIVEN
        discussion = {'title': 'some title', 'content': 'some content'}
        # WHEN
        post_response = api_client.post(reverse("discussions_app:discussions-list"), discussion)
        get_response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert post_response.status_code == 401, "Status code of response must be 401"
        assert len(get_response.json()) == 0, "The response must contain no discussions"

    def test_create_with_authenticated_user(self, api_client, user):
        # GIVEN
        discussion = {'title': 'some title', 'content': 'some content'}
        api_client.force_authenticate(user=user)
        # WHEN
        post_response = api_client.post(reverse("discussions_app:discussions-list"), discussion)
        get_response = api_client.get(reverse("discussions_app:discussions-list"))
        # THEN
        assert post_response.status_code == 201, "Status code of response must be 201"
        assert post_response.json().get('user') == str(user.id), "The response object must belong to the given user"
        assert len(get_response.json()) == 1, "The response must contain one discussion"

    # UPDATE
    def test_update_with_unauthenticated_user(self, api_client):
        # GIVEN
        new_discussion = {'title': 'new title', 'content': 'new content'}
        discussion = baker.make("discussions.Discussion")
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('title') != 'new title', "The response object must not contain 'new title'"

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        new_discussion = {'title': 'new title', 'content': 'new content'}
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('title') != 'new title', "The response object must not contain 'new title'"

    def test_update_with_owner(self, api_client, owner):
        # GIVEN
        new_discussion = {'title': 'new title', 'content': 'new content'}
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('title') == 'new title', "The response object must contain 'new title'"

    def test_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        new_discussion = {'title': 'new title', 'content': 'new content'}
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('title') == 'new title', "The response object must contain 'new title'"

    # PARTIAL UPDATE
    def test_partial_update_with_unauthenticated_user(self, api_client):
        # GIVEN
        partial_discussion = {'title': 'new title'}
        discussion = baker.make("discussions.Discussion")
        # WHEN
        response = api_client.patch(reverse("discussions_app:discussions-detail", args=(discussion.id,)), partial_discussion)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('title') != 'new title', "The response object must not contain 'new title'"
