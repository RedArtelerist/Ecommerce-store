# Generated by Django 3.1.4 on 2021-04-05 19:59

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_profile', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserProfile',
            new_name='Profile',
        ),
    ]