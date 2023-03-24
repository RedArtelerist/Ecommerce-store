# Generated by Django 4.1.7 on 2023-03-07 23:55

from django.db import migrations, models
import store.validations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0022_auto_20210529_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.png', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='imageitem',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.jpg', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/placeholder.jpg', null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.PositiveSmallIntegerField(default=2023, validators=[store.validations.validate_product_year], verbose_name='Year'),
        ),
    ]