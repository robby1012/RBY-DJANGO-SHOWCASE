from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from library.models import BookLog
from library.src.serializer.inquiry import InquiryCreateSerializer, InquiryUpdateSerializer


class _ViewSet(ModelViewSet):
    _route_location = r"inquiry"
    _route_name      = "library.inquiry"

    queryset           = BookLog.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return InquiryUpdateSerializer

        return InquiryCreateSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
