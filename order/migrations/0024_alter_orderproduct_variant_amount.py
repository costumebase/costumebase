# Generated by Django 3.2.4 on 2021-07-19 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0023_alter_orderproduct_variant_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='variant_amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
