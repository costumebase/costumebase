# Generated by Django 3.2.4 on 2021-06-16 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210616_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='discription',
            field=models.CharField(default='We provide', max_length=250),
            preserve_default=False,
        ),
    ]
