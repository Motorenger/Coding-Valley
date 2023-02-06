import pytest
from django.urls import reverse
from model_bakery import baker

from reviews.models import Review


pytestmark = pytest.mark.django_db


class TestReviewViewSet:
    # LIST
    def test_list_with_unauthenticated_user_with_no_reviews(self, api_client):
        # WHEN
        response = api_client.get(reverse("reviews_app:reviews-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_unauthenticated_user(self, api_client):
        # GIVEN
        baker.make("reviews.Review")
        # WHEN
        response = api_client.get(reverse("reviews_app:reviews-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_authenticated_user(self, api_client, user):
        # GIVEN
        baker.make("reviews.Review")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("reviews_app:reviews-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    # RETRIEVE
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # GIVEN
        review = baker.make("reviews.Review")
        # WHEN
        response = api_client.get(reverse("reviews_app:reviews-detail", args=(review.id,)))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # GIVEN
        review = baker.make("reviews.Review")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("reviews_app:reviews-detail", args=(review.id,)))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    # CREATE
    def test_create_with_unauthenticated_user(self, api_client):
        # GIVEN
        review = {"title": "some title", "content": "some content", "stars": 5}
        # WHEN
        response = api_client.post(reverse("reviews_app:reviews-list"), review)
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert reviews_number == 0, "There must be no reviews"

    def test_create_with_authenticated_user(self, api_client, user):
        # GIVEN
        review = {"title": "some title", "content": "some content", "stars": 5}
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.post(reverse("reviews_app:reviews-list"), review)
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 201, "Status code of response must be 201"
        assert response.json().get('user') == str(user.id), "The response object must belong to the given user"
        assert reviews_number == 1, "There must be one review"

    # UPDATE
    def test_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        new_review = {"title": "new title", "content": "new content", "stars": 1}
        # WHEN
        response = api_client.put(reverse("reviews_app:reviews-detail", args=(review.id,)), new_review)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        new_review = {"title": "new title", "content": "new content", "stars": 1}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviews-detail", args=(review.id,)), new_review)
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_update_with_owner(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        new_review = {"title": "new title", "content": "new content", "stars": 1}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviews-detail", args=(review.id,)), new_review)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        new_review = {"title": "new title", "content": "new content", "stars": 1}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviews-detail", args=(review.id,)), new_review)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # PARTIAL UPDATE
    def test_partial_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        partial_review = {'content': 'new content'}
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviews-detail", args=(review.id,)), partial_review)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviews-detail", args=(review.id,)), partial_review)
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert response.json().get('content') != 'new content', "The response object must not contain 'new content'"

    def test_partial_update_with_owner(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviews-detail", args=(review.id,)), partial_review)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    def test_partial_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviews-detail", args=(review.id,)), partial_review)
        # THEN
        assert response.status_code == 200, "Status code of response must be 200"
        assert response.json().get('content') == 'new content', "The response object must contain 'new content'"

    # DESTROY
    def test_destroy_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviews-detail", args=(review.id,)))
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert reviews_number == 1, "There must be one review"

    def test_destroy_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviews-detail", args=(review.id,)))
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert reviews_number == 1, "There must be one review"

    def test_destroy_with_owner(self, api_client, owner):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviews-detail", args=(review.id,)))
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert reviews_number == 0, "There must be no reviews"

    def test_destroy_with_admin(self, api_client, owner, admin):
        # GIVEN
        review = baker.prepare("reviews.Review")
        review.user = owner
        review.save()
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviews-detail", args=(review.id,)))
        reviews_number = Review.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert reviews_number == 0, "There must be no reviews"
