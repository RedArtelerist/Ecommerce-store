# Generated by Django 3.1.4 on 2021-03-06 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_likedislike'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='stock',
        ),
    ]