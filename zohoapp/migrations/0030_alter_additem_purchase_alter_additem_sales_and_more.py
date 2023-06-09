# Generated by Django 4.1.7 on 2023-05-28 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('zohoapp', '0029_payment_terms'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additem',
            name='purchase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.purchase'),
        ),
        migrations.AlterField(
            model_name='additem',
            name='sales',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.sales'),
        ),
        migrations.AlterField(
            model_name='additem',
            name='unit',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.unit'),
        ),
    ]
