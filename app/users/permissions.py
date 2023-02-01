from rest_framework import permissions


class IsOwnerOrSuperuser(permissions.BasePermission):
    @staticmethod
    def _is_superuser(request):
        return request.user.is_superuser

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or self._is_superuser(request)


class IsOwnerOrIsAdminOrReadOnly(permissions.BasePermission):
    """Allow to the object be updated or deleted either owner or admin.

    Other users can only read the object.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user == obj.user or request.user.is_superuser
