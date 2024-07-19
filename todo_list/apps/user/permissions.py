from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Allows access only to owner or admin users.
    """

    def has_permission(self, request, view):
        user_id = view.kwargs.get("user_id", 0)
        return request.user.is_staff or user_id == request.user.id
