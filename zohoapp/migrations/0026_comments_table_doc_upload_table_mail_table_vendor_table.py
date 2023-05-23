# Generated by Django 3.2.18 on 2023-05-08 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zohoapp', '0025_auto_20230420_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='vendor_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salutation', models.CharField(max_length=25)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=150)),
                ('vendor_display_name', models.CharField(max_length=150)),
                ('vendor_email', models.CharField(max_length=250)),
                ('vendor_wphone', models.CharField(max_length=50)),
                ('vendor_mphone', models.CharField(max_length=50)),
                ('skype_number', models.CharField(max_length=50)),
                ('designation', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('website', models.CharField(max_length=250)),
                ('gst_treatment', models.CharField(max_length=100)),
                ('gst_number', models.CharField(max_length=50, null=True)),
                ('pan_number', models.CharField(max_length=50, null=True)),
                ('source_supply', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=50)),
                ('opening_bal', models.CharField(max_length=100)),
                ('payment_terms', models.CharField(max_length=100)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='mail_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail_from', models.TextField(max_length=300)),
                ('mail_to', models.TextField(max_length=300)),
                ('subject', models.TextField(max_length=250)),
                ('content', models.TextField(max_length=900)),
                ('mail_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.vendor_table')),
            ],
        ),
        migrations.CreateModel(
            name='doc_upload_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=200)),
                ('document', models.FileField(upload_to='doc/')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.vendor_table')),
            ],
        ),
        migrations.CreateModel(
            name='comments_table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vendor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='zohoapp.vendor_table')),
            ],
        ),
    ]