# Generated by Django 4.1.7 on 2023-03-20 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0017_alter_order_paymentmethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='telegram_id',
            field=models.IntegerField(default=-1),
        ),
    ]
