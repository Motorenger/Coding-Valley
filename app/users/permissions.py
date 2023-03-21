from rest_framework import permissions


class IsOwnerOrIsAdminOrReadOnly(permissions.BasePermission):
    """
    Allows the object to be updated or deleted by object's owner or admin.
    Other users can only read the object.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_superuser


class EmailVerified(IsOwnerOrIsAdminOrReadOnly):
    def has_permission(self, request, view):
        """Object can be created only by user whose email was verified"""
        return request.user.email_vierified
