from rest_framework.permissions import BasePermission


# Владелец ли
class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        
        if obj.id == request.user.id:
            return True
        else:
            return False


# Администратор ли
class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        if request.user.is_admin:
            return True
        else:
            return False


# Модератор ли
class IsModerator(BasePermission):

    def has_permission(self, request, view):
        
        if request.user.is_moderator or request.user.is_admin:
            return True
        else:
            return False
