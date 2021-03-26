# Generated by Django 3.1.4 on 2021-02-12 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_comment_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-updated',)},
        ),
        migrations.AddField(
            model_name='review',
            name='advantages',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='review',
            name='disadvantages',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]