# Generated by Django 3.1.4 on 2021-03-07 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20210307_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='payment',
            new_name='paymentMethod',
        ),
    ]
