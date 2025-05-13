from django.contrib.auth import logout, get_user_model
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from simplelib.src.permissions import UnAuthorized


class _GenericApiView(ObtainAuthToken):
    _route_location = r'token/'
    _route_name     = 'authentication.token'

    _generic_view = True

    permission_classes_by_action = {
        'post'  : (UnAuthorized, ),
        'get'   : (IsAuthenticated, ),
        'delete': (IsAuthenticated, )
    }

    def get(self, request):
        response = {
            'first_name': request.user.first_name,
            'last_name' : request.user.last_name,
            'username'  : request.user.username,
            'email'     : request.user.email
        }
        return Response(response, status=HTTP_200_OK)

    def delete(self, request):
        """
        Delete method to remove token from authentication

        Args:
            request: request context from client

        Returns:
            Response object to client
        """
        request.user.auth_token.delete()
        logout(request)

        return Response({}, status=HTTP_200_OK)