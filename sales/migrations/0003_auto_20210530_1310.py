# Generated by Django 3.1.7 on 2021-05-30 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_auto_20210529_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='Position',
            new_name='positions',
        ),
    ]
