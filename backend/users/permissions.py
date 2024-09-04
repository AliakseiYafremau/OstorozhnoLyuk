from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if obj.id == request.user.id:
            return True
        else:
            return False


class IsAdmin(BasePermission):

    def has_permission(self, request, view, obj):

        if request.user.is_admin:
            return True
        else:
            return False


class IsModerator(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if request.user.is_moderator or request.user.is_admin:
            return True
        else:
            return False
