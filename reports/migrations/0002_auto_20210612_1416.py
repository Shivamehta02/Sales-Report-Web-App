# Generated by Django 3.1.7 on 2021-06-12 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterField(
            model_name='report',
            name='created',
            field=models.DateTimeField(editable=False),
        ),
        migrations.AlterField(
            model_name='report',
            name='updated',
            field=models.DateTimeField(),
        ),
    ]
