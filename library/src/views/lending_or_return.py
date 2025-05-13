from rest_framework.viewsets import ModelViewSet

from library.models import BookLog
from library.src.serializer.lending_or_return import LendingOrReturnSerializer
from simplelib.src.permissions import StaffModifiedOnly


class _ViewSet(ModelViewSet):
    _route_location = r"lending_or_return"
    _route_name      = "library.lending_or_return"

    queryset           = BookLog.objects.all()
    permission_classes = (StaffModifiedOnly, )
    serializer_class   = LendingOrReturnSerializer

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
