# Generated by Django 3.2.4 on 2021-07-19 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_alter_orderproduct_variant_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variant_amount',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
    ]
