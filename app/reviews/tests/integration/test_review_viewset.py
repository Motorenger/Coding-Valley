import pytest
from django.urls import reverse
from model_bakery import baker

from reviews.models import Review


pytestmark = pytest.mark.django_db


class TestReviewViewSet:
    # list
    def test_list_with_unauthenticated_user_with_no_reviews(self, api_client):
        # when
        response = api_client.get(reverse('reviews_app:reviews-list'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_list_with_unauthenticated_user(self, api_client):
        # given
        baker.make('reviews.Review')
        # when
        response = api_client.get(reverse('reviews_app:reviews-list'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_list_with_authenticated_user(self, api_client, user):
        # given
        baker.make('reviews.Review')
        api_client.force_authenticate(user=user)
        # when
        response = api_client.get(reverse('reviews_app:reviews-list'))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    # retrieve
    def test_retrieve_with_unauthenticated_user(self, api_client):
        # given
        review = baker.make('reviews.Review')
        # when
        response = api_client.get(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    def test_retrieve_with_authenticated_user(self, api_client, user):
        # given
        review = baker.make('reviews.Review')
        api_client.force_authenticate(user=user)
        # when
        response = api_client.get(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 405, 'Status code of response must be 405'

    # create
    def test_create_with_unauthenticated_user(self, api_client):
        # given
        media = baker.make('watchlists.Media')
        review = {'media': media.id, 'title': 'some title', 'content': 'some content', 'stars': 5}
        # when
        response = api_client.post(reverse('reviews_app:reviews-list'), review)
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert Review.objects.count() == 0, 'The db must contain no reviews'

    def test_create_with_authenticated_user(self, api_client, user):
        # given
        media = baker.make('watchlists.Media')
        review = {'media': media.id, 'title': 'some title', 'content': 'some content', 'stars': 5}
        api_client.force_authenticate(user=user)
        # when
        response = api_client.post(reverse('reviews_app:reviews-list'), review)
        # then
        assert response.status_code == 201, 'Status code of response must be 201'
        assert response.json().get('user') == str(user.id), 'The response object must belong to the given user'
        assert Review.objects.count() == 1, 'The db must contain one review'

    # update
    def test_update_with_unauthenticated_user(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        new_review = {'title': 'new title', 'content': 'new content', 'stars': 1}
        # when
        response = api_client.put(reverse('reviews_app:reviews-detail', args=(review.id,)), new_review)
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert response.json().get('content') != 'new content', 'The response object must not contain "new content"'

    def test_update_with_not_owner(self, api_client, owner, not_owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        new_review = {'title': 'new title', 'content': 'new content', 'stars': 1}
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.put(reverse('reviews_app:reviews-detail', args=(review.id,)), new_review)
        # then
        assert response.status_code == 403, 'Status code of response must be 403'
        assert response.json().get('content') != 'new content', 'The response object must not contain "new content"'

    def test_update_with_owner(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        new_review = {'title': 'new title', 'content': 'new content', 'stars': 1}
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.put(reverse('reviews_app:reviews-detail', args=(review.id,)), new_review)
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('content') == 'new content', 'The response object must contain "new content"'

    def test_update_with_admin(self, api_client, owner, admin):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        new_review = {'title': 'new title', 'content': 'new content', 'stars': 1}
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.put(reverse('reviews_app:reviews-detail', args=(review.id,)), new_review)
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('content') == 'new content', 'The response object must contain "new content"'

    # partial update
    def test_partial_update_with_unauthenticated_user(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        partial_review = {'content': 'new content'}
        # when
        response = api_client.patch(reverse('reviews_app:reviews-detail', args=(review.id,)), partial_review)
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert response.json().get('content') != 'new content', 'The response object must not contain "new content"'

    def test_partial_update_with_not_owner(self, api_client, owner, not_owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.patch(reverse('reviews_app:reviews-detail', args=(review.id,)), partial_review)
        # then
        assert response.status_code == 403, 'Status code of response must be 403'
        assert response.json().get('content') != 'new content', 'The response object must not contain "new content"'

    def test_partial_update_with_owner(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.patch(reverse('reviews_app:reviews-detail', args=(review.id,)), partial_review)
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('content') == 'new content', 'The response object must contain "new content"'

    def test_partial_update_with_admin(self, api_client, owner, admin):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        partial_review = {'content': 'new content'}
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.patch(reverse('reviews_app:reviews-detail', args=(review.id,)), partial_review)
        # then
        assert response.status_code == 200, 'Status code of response must be 200'
        assert response.json().get('content') == 'new content', 'The response object must contain "new content"'

    # destroy
    def test_destroy_with_unauthenticated_user(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        # when
        response = api_client.delete(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 401, 'Status code of response must be 401'
        assert Review.objects.count() == 1, 'The db must contain one review'

    def test_destroy_with_not_owner(self, api_client, owner, not_owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        api_client.force_authenticate(user=not_owner)
        # when
        response = api_client.delete(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 403, 'Status code of response must be 403'
        assert Review.objects.count() == 1, 'The db must contain one review'

    def test_destroy_with_owner(self, api_client, owner):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        api_client.force_authenticate(user=owner)
        # when
        response = api_client.delete(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 204, 'Status code of response must be 204'
        assert Review.objects.count() == 0, 'The db must contain no reviews'

    def test_destroy_with_admin(self, api_client, owner, admin):
        # given
        review = baker.prepare('reviews.Review')
        review.user = owner
        review.media = baker.make('watchlists.Media')
        review.save()
        api_client.force_authenticate(user=admin)
        # when
        response = api_client.delete(reverse('reviews_app:reviews-detail', args=(review.id,)))
        # then
        assert response.status_code == 204, 'Status code of response must be 204'
        assert Review.objects.count() == 0, 'The db must contain no reviews'
