"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.permissions import AllowAny
from users.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users.views import UserView, LoginView, ListUsersView, UpdateDeleteUserView, ChangeAdminView


schema_view = get_schema_view(
    openapi.Info(
        title="OstorozhnoLyuk API",
        default_version='v1',
        description="API for OstorozhnoLyuk",
        terms_of_service="htttps://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('account/admin/', admin.site.urls),
    path('account/user/', UserView.as_view(), name='user'), # Получание текущего пользователя.
    path('account/user/<int:pk>/', UpdateDeleteUserView.as_view(), name='update_delete_user'), # Для администратора. Получаение пользователя по id. Изменение, удаление.
    path('account/users/', ListUsersView.as_view(), name='list_users'), # Для администратора. Получение списка пользователей.
    path('account/change_admin/', ChangeAdminView.as_view(), name='change_admin'),

    path('account/login/', LoginView.as_view(), name='login'),
    
    path('account/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('account/api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('account/swagger/<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('account/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('account/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
