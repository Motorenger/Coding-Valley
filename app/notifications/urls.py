from django.urls import path

from . import views

urlpatterns = [
    path("<str:uuid>", views.ReadNotificationView.as_view(), name="read-notification"),
    path("", views.GetNotificationView.as_view(), name="get-notification"),
]
