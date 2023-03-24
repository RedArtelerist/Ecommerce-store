# Generated by Django 4.1.7 on 2023-03-08 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0010_usercart_message_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercart',
            name='chat_id',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='usercart',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
