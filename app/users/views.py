import logging

import requests

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.managers import UserManager
from users.models import User, UserProfile
from users.serializers import (ChangePasswordSerializer, RegisterSerializer,
                               UpdateProfileSerializer, UserProfileSerializer,
                               UserSerializer, UserTokenObtainPairSerializer)
from watchlists.models import Media
from notifications.models import Notification


logger = logging.getLogger(__name__)


class LoginView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LogoutView(APIView):
    """
    Logout user from current session
    using blacklist RefreshToken method.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'users/logout: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    """
    Logout user from all sessions
    using blacklist OutstandigToken method.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.user.id
            tokens = OutstandingToken.objects.filter(user_id=user_id)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f'users/logout_all: {e}')
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GoogleView(APIView):
    """
    Sign in or Sign up user using OAuth2.
    """
    def post(self, request):
        payload = {'access_token': request.data.get("token")}
        request = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)

        if 'error' in (data := json.loads(request.text)):
            response = {'message': 'wrong google token / this google token is already expired.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            user = User()
            user.email = data['email']
            user.first_name = data['given_name']
            user.last_name = data['family_name']
            user.password = make_password(UserManager().make_random_password())
            user.save()

        token = RefreshToken.for_user(user)
        response = {}
        response['email'] = user.email
        response['username'] = user.username
        response['access_token'] = str(token.access_token)
        response['refresh_token'] = str(token)
        return Response(response, status=status.HTTP_302_FOUND)


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60*24*90, key_prefix='userprofile_cache'))
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def get_object(self, **kwargs):
        return User.objects.get(username=self.kwargs['username'])


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user


class ChangePasswordView(UpdateAPIView):
    """
    Allows user to change password in profile settings
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class FollowView(APIView):
    """
    Follow user with notification to followed user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        try:
            user = request.user
            to_user = User.objects.get(username=username)
            profile = to_user.userprofile
            if user == to_user:
                return Response('You can’t follow yourself', status=status.HTTP_400_BAD_REQUEST)

            if user in profile.followers.all():
                profile.followers.remove(user)
                profile.followers_count = profile.followers.count()
                profile.save()
                return Response('User unfollowed', status=status.HTTP_204_NO_CONTENT)
            else:
                profile.followers.add(user)
                profile.followers_count = profile.followers.count()
                profile.save()
                Notification.objects.create(
                    to_user=to_user,
                    created_by=user,
                    notification_type='follow',
                    followed_by=user,
                    content=f"{user.userprofile.user} started following you."
                )
                return Response('User followed', status=status.HTTP_200_OK)
        except Exception as e:
            message = {'detail': f'{e}'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class FavouritesView(APIView):
    """
    Follow user with notification to followed user
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        try:
            media = Media.objects.get(id=uuid)
            profile = request.user.userprofile

            if media in profile.favourites.all():
                profile.favourites.remove(media)
                profile.favourites_count = profile.favourites.count()
                profile.save()
                return Response('Removed from favourites', status=status.HTTP_204_NO_CONTENT)
            else:
                profile.favourites.add(media)
                profile.favourites_count = profile.favourites.count()
                profile.save()
                return Response('Added to favourites', status=status.HTTP_200_OK)
        except Exception as e:
            message = {'detail': f'{e}'}
            return Response(message, status=status.HTTP_204_NO_CONTENT)


class SendEmailView(APIView):
    """
    Sends an activation link via email to requested user.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.email_verified:
            return Response('Your email is already activated', status=status.HTTP_403_FORBIDDEN)
        try:
            title = 'Verify your Valley account.'
            message = render_to_string('verify-email.html', {
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = user.email
            email = EmailMultiAlternatives(title, message, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.send()
            return Response('Activation email was sent successfully.', status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Activation email: {e}')
            return Response({'detail': f'{e}'}, status=status.HTTP_403_FORBIDDEN)


class ActivateEmail(APIView):
    """
    Verifiy user email via link.
    """

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            user = None
            logger.error(f'Activation email: {e}')

        if user is None:
            return Response('Something went wrong , please try again', status=status.HTTP_406_NOT_ACCEPTABLE)
        if user.email_verified:
            return Response('Your email is already verified.', status=status.HTTP_406_NOT_ACCEPTABLE)
        if not default_token_generator.check_token(user, token):
            return Response('Something went wrong, please try again', status=status.HTTP_406_NOT_ACCEPTABLE)

        user.email_verified = True
        user.save()
        return Response("You email was sucessfuly verified.")
