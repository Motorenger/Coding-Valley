from django.urls import path

from notifications import views


urlpatterns = [
    path("", views.GetNotificationView.as_view(), name="get-notification"),
    path("<str:uuid>", views.ReadNotificationView.as_view(), name="read-notification"),
]
