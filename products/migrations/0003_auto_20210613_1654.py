# Generated by Django 3.2.4 on 2021-06-13 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210613_1651'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'verbose_name_plural': '6. Colors'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name_plural': '9. Comments'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': '1. Products'},
        ),
        migrations.AlterModelOptions(
            name='size',
            options={'verbose_name_plural': '7. Sizes'},
        ),
    ]
