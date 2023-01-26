from rest_framework.viewsets import ModelViewSet

from ..models import Discussion
from .serializers import DiscussionSerializer


class DiscussionsViewSet(ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
