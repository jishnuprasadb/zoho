# Generated by Django 4.1.7 on 2023-05-29 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0037_rename_inv_sales_item_sale'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salesorder',
            old_name='d_mathod',
            new_name='d_method',
        ),
    ]
