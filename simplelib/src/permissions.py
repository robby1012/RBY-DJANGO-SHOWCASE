from rest_framework.permissions import BasePermission


class UnAuthorized(BasePermission):
    """
    Only allow the Non-Authenticated user
    """
    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class StaffModifiedOnly(BasePermission):
    """
    Only allow the staff when it comes to action modification such as save, update, or delete
    """
    def has_permission(self, request, view):
        if view.action in ('create', 'update', 'destroy'):
            return request.user.is_staff
        else:
            return True
