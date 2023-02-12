import pytest
from django.urls import reverse
from model_bakery import baker

from watchlists.models import Media
from watchlists.serializers import MediaSerializer


pytestmark = pytest.mark.django_db


def test_get(api_client):
    # given
    for _ in range(10):
        baker.make("watchlists.Media")
    db_data = Media.objects.order_by('-last_retrieved')
    serialized_data = MediaSerializer(db_data, many=True).data
    # when
    test_response = api_client.get(reverse("watchlists_app:recently_searched"))
    # then
    assert serialized_data == test_response.json(), "The serialized data must be equal to the response data"
    assert test_response.status_code == 200, "Status code of response must be 200"


def test_post(api_client):
    # when
    test_response = api_client.post(reverse("watchlists_app:recently_searched"), {})
    # then
    assert test_response.status_code == 405, "Status code of response must be 405"
