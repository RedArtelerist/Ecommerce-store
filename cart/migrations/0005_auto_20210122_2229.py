# Generated by Django 3.1.4 on 2021-01-22 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20210122_2226'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercart',
            old_name='items',
            new_name='items_cart',
        ),
    ]
