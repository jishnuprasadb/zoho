# Generated by Django 4.1.7 on 2023-05-28 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0030_alter_additem_purchase_alter_additem_sales_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additem',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
