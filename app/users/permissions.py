from rest_framework import permissions


class IsOwnerOrSuperuser(permissions.BasePermission):
    @staticmethod
    def _is_superuser(request):
        return request.user.is_superuser 

    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or self._is_superuser(request)
