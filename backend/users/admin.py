from django.contrib import admin
from django.http import HttpRequest
from .models import User


class UserAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        if not request.user.is_authenticated:
            return False
        return request.user.is_admin


admin.site.register(User, UserAdmin)
