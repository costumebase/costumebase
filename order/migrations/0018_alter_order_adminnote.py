# Generated by Django 3.2.4 on 2021-07-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_auto_20210713_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='adminnote',
            field=models.TextField(blank=True),
        ),
    ]
