from drf_yasg import openapi


header_param = openapi.Parameter(
    name='Authorization',
    in_=openapi.IN_HEADER,
    description=r'JWT токен аутентификации. Использовать формат <b>Bearer {token}</b>',
    type=openapi.TYPE_STRING,
)

id_param = openapi.Parameter(
    name='id',
    in_=openapi.IN_PATH,
    description='ID пользователя',
    type=openapi.TYPE_INTEGER,
)

id_scheme = openapi.Schema(
    type=openapi.TYPE_INTEGER,
    description='ID пользователя')

email_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='Почта пользователя')

password_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='Пароль пользователя')

is_moderator_schema = openapi.Schema(
    type=openapi.TYPE_BOOLEAN,
    description='Модератор или нет')

is_admin_schema = openapi.Schema(
    type=openapi.TYPE_BOOLEAN,
    description='Админ или нет')

token_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='Токен аутентификации')

refresh_token_schema = openapi.Schema(
    type=openapi.TYPE_STRING,
    description='Токен обновления')