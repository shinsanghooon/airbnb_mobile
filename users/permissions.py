from rest_framework.permissions import BasePermission

class IsSelf(BasePermission):
    # single object에 접근
    def has_object_permission(self, request, view, user):
        return user == request.user
