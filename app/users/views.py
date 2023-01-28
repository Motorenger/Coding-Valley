from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers import UserTokenObtainPairSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routes = [
        'token/',
        'token/refresh/',
    ]
    return Response(routes)
