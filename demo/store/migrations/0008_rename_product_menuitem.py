# Generated by Django 3.2.8 on 2021-10-27 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_auto_20211025_2344'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product',
            new_name='MenuItem',
        ),
    ]