# Generated by Django 5.1.3 on 2024-11-24 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plantillas', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='archivoentrada',
            name='usuario',
        ),
    ]
