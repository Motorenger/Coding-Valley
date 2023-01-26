from django.urls import path, include
from rest_framework.routers import SimpleRouter

from discussions.api.viewsets import DiscussionsViewSet, CommentViewSet

router = SimpleRouter()
router.register(r'discussions', DiscussionsViewSet, basename='discussions')
router.register(r'comments', CommentViewSet, basename='comments')

app_name = "discussions"

urlpatterns = [
    path('', include(router.urls)),
]
