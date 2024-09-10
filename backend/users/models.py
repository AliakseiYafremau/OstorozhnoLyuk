from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

# Модель пользователя
class User(AbstractBaseUser):
    # username = models.CharField(max_length=150,
    #                             unique=True,
    #                             error_messages={
    #                                 'required': 'Поле обязательно к заполнению',
    #                                 'unique': 'Имя пользователя уже занято'
    #                             })

    email = models.EmailField(unique=True,
                              error_messages={
                                  'required': 'Поле обязательно к заполнению',
                                  'unique': 'Email уже занят'
                              })
    is_moderator = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'
