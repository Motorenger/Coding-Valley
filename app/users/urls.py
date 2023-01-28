from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users import views


urlpatterns = [
    path('', views.getRoutes),
    path('token/', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
