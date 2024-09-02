from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


# Модель пользователя
class User(AbstractBaseUser):
    username = models.CharField(max_length=150,
                                unique=True,
                                error_messages={
                                    'unique': 'Имя пользователя уже занято'
                                })
    email = models.EmailField(required=True,
                              error_messages={
                                  'required': 'Поле обязательно к заполнению'
                              })
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
