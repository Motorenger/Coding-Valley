from django.urls import path, include
from rest_framework.routers import SimpleRouter

from discussions.viewsets import DiscussionViewSet, CommentViewSet

router = SimpleRouter()
router.register(r'discussions', DiscussionViewSet, basename='discussions')
router.register(r'comments', CommentViewSet, basename='comments')

app_name = "discussions"

urlpatterns = [
    path('', include(router.urls)),
]
