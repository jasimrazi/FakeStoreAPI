# Generated by Django 5.1.1 on 2024-11-11 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_rename_street_address_address_address'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='address',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='address',
            name='is_default',
        ),
    ]