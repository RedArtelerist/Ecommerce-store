# Generated by Django 3.1.4 on 2021-05-23 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0014_auto_20210524_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='description',
            field=models.TextField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.delivery'),
        ),
    ]
