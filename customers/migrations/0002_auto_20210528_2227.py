# Generated by Django 3.1.7 on 2021-05-28 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Customers',
            new_name='Customer',
        ),
    ]
