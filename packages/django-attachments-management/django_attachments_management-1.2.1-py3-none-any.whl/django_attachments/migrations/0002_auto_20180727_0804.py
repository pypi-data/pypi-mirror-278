# Generated by Django 2.0.6 on 2018-07-27 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_attachments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='caption',
            field=models.TextField(blank=True, verbose_name='Caption'),
        ),
        migrations.AddField(
            model_name='attachment',
            name='title',
            field=models.CharField(blank=True, max_length=255, verbose_name='Name'),
        ),
    ]
