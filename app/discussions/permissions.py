from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrIsAdminOrReadOnly(BasePermission):
    """Allow to the object be updated or deleted either owner or admin.
    
    Other users can only read the object."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user or request.user.is_superuser
