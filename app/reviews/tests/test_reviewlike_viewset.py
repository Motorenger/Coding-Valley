import pytest
from django.urls import reverse
from model_bakery import baker

from reviews.models import ReviewLikes


pytestmark = pytest.mark.django_db


class TestReviewLikesViewSet:
    # LIST
    def test_list_with_unauthenticated_user_with_no_reviewlikes(self, api_client):
        # WHEN
        response = api_client.get(reverse("reviews_app:reviewlikes-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_unauthenticated_user(self, api_client):
        # GIVEN
        baker.make("reviews.ReviewLikes")
        # WHEN
        response = api_client.get(reverse("reviews_app:reviewlikes-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_list_with_authenticated_user(self, api_client, user):
        # GIVEN
        baker.make("reviews.ReviewLikes")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("reviews_app:reviewlikes-list"))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    # RETRIEVE
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # GIVEN
        reviewlike = baker.make("reviews.ReviewLikes")
        # WHEN
        response = api_client.get(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # GIVEN
        reviewlike = baker.make("reviews.ReviewLikes")
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.get(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"

    # CREATE
    def test_create_with_unauthenticated_user(self, api_client):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = {"review": review.id, "like": "true"}
        # WHEN
        response = api_client.post(reverse("reviews_app:reviewlikes-list"), reviewlike)
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert reviewlikes_number == 0, "There must be no reviewlikes"

    def test_create_with_authenticated_user(self, api_client, user):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = {"review": review.id, "like": "true"}
        api_client.force_authenticate(user=user)
        # WHEN
        response = api_client.post(reverse("reviews_app:reviewlikes-list"), reviewlike)
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 201, "Status code of response must be 201"
        assert response.json().get('user') == str(user.id), "The response object must belong to the given user"
        assert reviewlikes_number == 1, "There must be one reviewlike"

    # UPDATE
    def test_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = review
        reviewlike.save()
        new_reviewlike = {"review": review.id, "like": "false"}
        # WHEN
        response = api_client.put(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = review
        reviewlike.save()
        new_reviewlike = {"review": review.id, "like": "false"}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_update_with_owner(self, api_client, owner):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = review
        reviewlike.save()
        new_reviewlike = {"review": review.id, "like": "false"}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        review = baker.make("reviews.Review")
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = review
        reviewlike.save()
        new_reviewlike = {"review": review.id, "like": "false"}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.put(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    # PARTIAL UPDATE
    def test_partial_update_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        new_reviewlike = {"like": "false"}
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_partial_update_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        new_reviewlike = {"like": "false"}
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_partial_update_with_owner(self, api_client, owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        new_reviewlike = {"like": "false"}
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    def test_partial_update_with_admin(self, api_client, owner, admin):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        new_reviewlike = {"like": "false"}
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.patch(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)), new_reviewlike)
        # THEN
        assert response.status_code == 405, "Status code of response must be 405"
        assert response.json().get('like') is not False, "The response object must not contain 'false'"

    # DESTROY
    def test_destroy_with_unauthenticated_user(self, api_client, owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 401, "Status code of response must be 401"
        assert reviewlikes_number == 1, "There must be one reviewlike"

    def test_destroy_with_not_owner(self, api_client, owner, not_owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        api_client.force_authenticate(user=not_owner)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 403, "Status code of response must be 403"
        assert reviewlikes_number == 1, "There must be one reviewlike"

    def test_destroy_with_owner(self, api_client, owner):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        api_client.force_authenticate(user=owner)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert reviewlikes_number == 0, "There must be no reviewlikes"

    def test_destroy_with_admin(self, api_client, owner, admin):
        # GIVEN
        reviewlike = baker.prepare("reviews.ReviewLikes")
        reviewlike.user = owner
        reviewlike.review = baker.make("reviews.Review")
        reviewlike.save()
        api_client.force_authenticate(user=admin)
        # WHEN
        response = api_client.delete(reverse("reviews_app:reviewlikes-detail", args=(reviewlike.id,)))
        reviewlikes_number = ReviewLikes.objects.count()
        # THEN
        assert response.status_code == 204, "Status code of response must be 204"
        assert reviewlikes_number == 0, "There must be no reviewlikes"
