# Generated by Django 4.1.7 on 2023-05-29 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0036_sales_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales_item',
            old_name='inv',
            new_name='sale',
        ),
    ]