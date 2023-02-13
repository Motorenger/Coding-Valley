from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users import views


app_name = 'users_app'


urlpatterns = [
    # authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('google/authenticate/', views.GoogleView.as_view(), name='google_auth'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('email/verify/send/', views.SendEmailView.as_view(), name='send-activation-email'),
    path('verify/<uidb64>/<token>/', views.ActivateEmail.as_view(), name='verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('logout/all/', views.LogoutAllView.as_view(), name='logout_all'),
    # profile
    path('profile/<str:username>', views.ProfileView.as_view(), name='profile'),
    path('update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    path('<str:username>/follow/', views.FollowView.as_view(), name="follow_user"),
    path('<str:uuid>/add/', views.FavouritesView.as_view(), name="add_favourites"),
]
