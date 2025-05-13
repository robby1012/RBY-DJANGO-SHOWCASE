from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from authentication.src.serializers.registration import RegistrationSerializer
from simplelib.src.permissions import UnAuthorized


class _ViewSet(ModelViewSet):
    _route_location = r"registration"
    _route_name     = "authentication.registration"

    queryset = get_user_model().objects.none()
    permission_classes = (UnAuthorized,)
    serializer_class = RegistrationSerializer
