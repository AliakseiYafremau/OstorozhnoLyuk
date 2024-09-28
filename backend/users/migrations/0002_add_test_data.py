# Generated by Django 5.1 on 2024-09-28 21:22

from django.db import migrations
from users.models import User


def create_test_data(apps, schema_editor):

    User.objects.create_user(email='user1@example.com', password='pass1',
                             is_moderator=False, is_admin=False)
    User.objects.create_user(email='user2@example.com', password='pass2',
                             is_moderator=False, is_admin=False)
    User.objects.create_user(email='user3@example.com', password='pass3',
                             is_moderator=False, is_admin=False)

    User.objects.create_user(email='moderator1@example.com', password='pass1',
                             is_moderator=True, is_admin=False)
    User.objects.create_user(email='moderator2@example.com', password='pass2',
                             is_moderator=True, is_admin=False)
    User.objects.create_user(email='moderator3@example.com', password='pass3',
                             is_moderator=True, is_admin=False)

    User.objects.create_user(email='admin@example.com', password='admin',
                             is_moderator=True, is_admin=True)

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_test_data)
    ]
