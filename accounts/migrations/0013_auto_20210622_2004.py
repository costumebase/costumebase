# Generated by Django 3.2.4 on 2021-06-22 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_buyer_email_confirmed'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='business_profile',
            options={'verbose_name_plural': '3. Vendor_Details'},
        ),
        migrations.AlterModelOptions(
            name='buyer',
            options={'verbose_name_plural': '4. Buyers'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': '1. Users'},
        ),
        migrations.AlterModelOptions(
            name='vendor',
            options={'verbose_name_plural': '2. Vendors'},
        ),
    ]
