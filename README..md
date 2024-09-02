# Начало работы:
- Для клонирования проекта используйте команду: 
    
    ```git clone <URL-адрес репозитория>```

- Перейдите в корневую папку проекта

- Для скачивания сторонних библиотек используйте команду:
    
    ```pip install -r requirements.txt```

# Запуск backend-части:
- Перейдите в папку backend

- Создание миграций и запустите:

    ```python manage.py makemigrations```
    ```python manage.py migrate```

- Запустите проект:

    ```python manage.py runserver```