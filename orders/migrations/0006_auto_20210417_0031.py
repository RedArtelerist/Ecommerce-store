# Generated by Django 3.1.4 on 2021-04-16 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20210314_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('Transferred to the carrier', 'Transferred to the carrier'), ('On the way', 'On the way'), ('Delivered', 'Delivered'), ('Received', 'Received'), ('Canceled', 'Canceled')], default='New', max_length=40),
        ),
    ]
