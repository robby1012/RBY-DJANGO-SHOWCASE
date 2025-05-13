from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authentication.models import Profile
from authentication.src.serializers.profile import ProfileSerializer


class _ViewSet(ModelViewSet):
    _route_location = r"profile"
    _route_name     = "authentication.profile"

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        queryset = Profile.objects.filter(user=self.request.user)
        return queryset
