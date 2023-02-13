import pytest
from django.urls import reverse
from model_bakery import baker

from discussions.models import Comment


pytestmark = pytest.mark.django_db


class TestCommentViewSet:
    # list
    def test_list_with_unauthenticated_user_with_no_comments(self, api_client):
        # when
        response = api_client.get(reverse("discussions_app:comments-list"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_unauthenticated_user(self, api_client):
        # given
        baker.make("discussions.Comment")
        # when
        response = api_client.get(reverse("discussions_app:comments-list"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_authenticated_user(self, api_client, user):
        # given
        baker.make("discussions.Comment")
        api_client.force_authenticate(user=user)
        # when
        response = api_client.get(reverse("discussions_app:comments-list"))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    # retrieve
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # given
        comment = baker.make("discussions.Comment")
        # when
        response = api_client.get(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # given
        comment = baker.make("discussions.Comment")
        api_client.force_authenticate(user=user)
        # when
        response = api_client.get(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 405, "Status code of response must be 405"

    # create
    def test_create_with_unauthenticated_user(self, api_client):
        # given
        discussion = baker.make("discussions.Discussion")
        comment = {"discussion": discussion.id, "content": "content for comment"}
        # when
        response = api_client.post(reverse("discussions_app:comments-list"), comment)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert Comment.objects.count() == 0, "The db must contain no comments"

    def test_create_with_authenticated_user(self, api_client, user):
        # given
        discussion = baker.make("discussions.Discussion")
        comment = {"discussion": discussion.id, "content": "content for comment"}
        api_client.force_authenticate(user=user)
        # when
        response = api_client.post(reverse("discussions_app:comments-list"), comment)
        # then
        assert response.status_code == 201, "Status code of response must be 201"
        assert response.json().get('user') == str(user.id), "The response object must belong to the given user"
        assert Comment.objects.count() == 1, "The db must contain one comment"

    # update
    def test_update_with_unauthenticated_user(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        new_comment = {'content': 'new content'}
        # when
        response = api_client.put(reverse("discussions_app:comments-detail", args=(comment.id,)), new_comment)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        new_comment = {'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.put(reverse("discussions_app:comments-detail", args=(comment.id,)), new_comment)
        # then
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_owner(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        new_comment = {'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.put(reverse("discussions_app:comments-detail", args=(comment.id,)), new_comment)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_update_with_admin(self, api_client, owner, admin):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        new_comment = {'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.put(reverse("discussions_app:comments-detail", args=(comment.id,)), new_comment)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # partial update
    def test_partial_update_with_unauthenticated_user(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        partial_comment = {'content': 'new content'}
        # when
        response = api_client.patch(reverse("discussions_app:comments-detail", args=(comment.id,)), partial_comment)
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_not_owner(self, api_client, owner, not_owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        partial_comment = {'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.patch(reverse("discussions_app:comments-detail", args=(comment.id,)), partial_comment)
        # then
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_owner(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        partial_comment = {'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.patch(reverse("discussions_app:comments-detail", args=(comment.id,)), partial_comment)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_partial_update_with_admin(self, api_client, owner, admin):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        partial_comment = {'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.patch(reverse("discussions_app:comments-detail", args=(comment.id,)), partial_comment)
        # then
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # destroy
    def test_destroy_with_unauthenticated_user(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        # when
        response = api_client.delete(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 401, "Status code of response must be 401"
        assert Comment.objects.count() == 1, "There must be one comment"

    def test_destroy_with_not_owner(self, api_client, owner, not_owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.delete(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 403, "Status code of response must be 403"
        assert Comment.objects.count() == 1, "There must be one comment"

    def test_destroy_with_owner(self, api_client, owner):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.delete(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 204, "Status code of response must be 204"
        assert Comment.objects.count() == 0, "The db must contain no comments"

    def test_destroy_with_admin(self, api_client, owner, admin):
        # given
        comment = baker.prepare("discussions.Comment")
        comment.user = owner
        comment.discussion = baker.make("discussions.Discussion")
        comment.save()
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.delete(reverse("discussions_app:comments-detail", args=(comment.id,)))
        # then
        assert response.status_code == 204, "Status code of response must be 204"
        assert Comment.objects.count() == 0, "The db must contain no comments"
