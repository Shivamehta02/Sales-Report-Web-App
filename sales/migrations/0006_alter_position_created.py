# Generated by Django 3.2.9 on 2022-10-26 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0005_auto_20210612_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='created',
            field=models.DateTimeField(blank=True, null=b'I01\n'),
        ),
    ]
