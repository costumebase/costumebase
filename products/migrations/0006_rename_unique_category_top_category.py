# Generated by Django 3.2.4 on 2021-06-16 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20210616_0915'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='unique',
            new_name='top_category',
        ),
    ]
