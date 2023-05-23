# Generated by Django 4.2 on 2023-04-18 06:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zohoapp', '0021_remove_history_product_additem_history'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additem',
            name='History',
        ),
        migrations.CreateModel(
            name='productHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.history')),
                ('p_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='zohoapp.additem')),
                ('p_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]