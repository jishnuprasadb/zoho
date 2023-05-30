# Generated by Django 4.1.7 on 2023-05-29 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0034_salesorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salesorder',
            name='s_date',
        ),
        migrations.AddField(
            model_name='salesorder',
            name='sales_date',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='salesorder',
            name='ship_date',
            field=models.DateField(blank=True, max_length=255, null=True),
        ),
    ]
