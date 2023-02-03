from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from discussions.models import Discussion, Comment
from discussions.serializers import DiscussionSerializer, DiscussionSerializerWithComments, CommentSerializer
from users.permissions import IsOwnerOrIsAdminOrReadOnly


class DiscussionViewSet(ModelViewSet):
    queryset = Discussion.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DiscussionSerializerWithComments
        return DiscussionSerializer


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
