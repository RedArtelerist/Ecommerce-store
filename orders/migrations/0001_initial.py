# Generated by Django 3.1.4 on 2021-03-06 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0016_remove_product_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_first_name', models.CharField(max_length=20)),
                ('customer_last_name', models.CharField(max_length=30)),
                ('customer_phone', models.CharField(max_length=15)),
                ('customer_email', models.EmailField(max_length=254)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=250)),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('Transferred to the carrier', 'Transferred to the carrier'), ('Delivering', 'Delivering'), ('Delivered to the department', 'Delivered to the department'), ('Received', 'Received'), ('Canceled', 'Canceled')], default='New', max_length=40)),
                ('delivery', models.CharField(choices=[('Courier', 'Courier'), ('Post office', 'Post office')], max_length=15)),
                ('payment', models.CharField(choices=[('Cash', 'Cash'), ('Card', 'Card'), ('PayPal', 'PayPal'), ('PrivatPay', 'PrivatPay')], max_length=20)),
                ('recipient_first_name', models.CharField(max_length=20)),
                ('recipient_last_name', models.CharField(max_length=30)),
                ('recipient_email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField(verbose_name='Price')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.product')),
            ],
        ),
    ]
