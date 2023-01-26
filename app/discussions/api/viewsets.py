from rest_framework.viewsets import ModelViewSet

from ..models import Discussion, Comment
from .serializers import DiscussionSerializer, CommentSerializer


class DiscussionViewSet(ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
