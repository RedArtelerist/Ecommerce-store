# Generated by Django 4.1.7 on 2023-03-16 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20210528_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paymentMethod',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card')], default='cash', max_length=20),
        ),
    ]
