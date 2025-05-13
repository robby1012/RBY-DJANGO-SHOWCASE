from rest_framework.viewsets import ModelViewSet

from library.models import Book
from library.src.serializer.book import BookSerializer
from simplelib.src.permissions import StaffModifiedOnly


class _ViewSet(ModelViewSet):
    _route_location = r"book"
    _route_name = "library.book"

    queryset = Book.objects.all().order_by('-created_at')
    permission_classes = (StaffModifiedOnly, )
    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
