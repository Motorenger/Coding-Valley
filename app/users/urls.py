from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from users import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/all/', views.LogoutAllView.as_view(), name='logout_all'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('<str:username>/follow/', views.FollowView.as_view(), name="follow_user"),
    path('<str:uuid>/add/', views.FavouritesView.as_view(), name="add_favourites"),
]
