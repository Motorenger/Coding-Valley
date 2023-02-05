import pytest
from django.urls import reverse
from model_bakery import baker

from discussions.models import Discussion


pytestmark = pytest.mark.django_db


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
        response = api_client.post(reverse("discussions_app:discussions-list"), discussion)
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert discussions_number == 0, "There must be no discussions"

    def test_create_with_authenticated_user(self, api_client, user):
        # GIVEN
        discussion = {'title': 'some title', 'content': 'some content'}
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.post(reverse("discussions_app:discussions-list"), discussion)
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 201, "Status code of response must be 201"
        assert response.json().get('user') == str(user.id), "The response object must belong to the given user"
        assert discussions_number == 1, "There must be one discussion"

    # UPDATE
    def test_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        new_discussion = {'title': 'new title', 'content': 'new content'}
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        new_discussion = {'title': 'new title', 'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_owner(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        new_discussion = {'title': 'new title', 'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        new_discussion = {'title': 'new title', 'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.put(reverse("discussions_app:discussions-detail", args=(discussion.id,)), new_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # PARTIAL UPDATE
    def test_partial_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        partial_discussion = {'content': 'new content'}
        # WHEN
        response = api_client.patch(reverse("discussions_app:discussions-detail", args=(discussion.id,)), partial_discussion)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        partial_discussion = {'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.patch(reverse("discussions_app:discussions-detail", args=(discussion.id,)), partial_discussion)
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_owner(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        partial_discussion = {'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.patch(reverse("discussions_app:discussions-detail", args=(discussion.id,)), partial_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_partial_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        partial_discussion = {'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.patch(reverse("discussions_app:discussions-detail", args=(discussion.id,)), partial_discussion)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # DESTROY
    def test_destroy_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        # WHEN
        response = api_client.delete(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert discussions_number == 1, "There must be one discussion"

    def test_destroy_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.delete(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert discussions_number == 1, "There must be one discussion"

    def test_destroy_with_owner(self, api_client, owner):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.delete(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert discussions_number == 0, "There must be no discussions"

    def test_destroy_with_admin(self, api_client, owner, admin):
        # GIVEN
        discussion = baker.prepare("discussions.Discussion")
        discussion.user = owner
        discussion.save()
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.delete(reverse("discussions_app:discussions-detail", args=(discussion.id,)))
        discussions_number = Discussion.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert discussions_number == 0, "There must be no discussions"
