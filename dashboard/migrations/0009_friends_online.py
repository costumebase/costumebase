# Generated by Django 3.2.4 on 2021-09-21 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_delete_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='friends',
            name='online',
            field=models.BooleanField(default=False),
        ),
    ]
