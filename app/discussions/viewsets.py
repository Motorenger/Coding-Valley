from rest_framework import mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from discussions.models import Discussion, Comment
from discussions.serializers import DiscussionSerializer, DiscussionSerializerWithComments, CommentSerializer, CommentSerializerForUpdate
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


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     GenericViewSet):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrIsAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        print('get_serializer_class', self.action)
        if self.action in ('update', 'partial_update'):
            return CommentSerializerForUpdate
        return CommentSerializer
