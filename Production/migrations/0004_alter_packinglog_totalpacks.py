# Generated by Django 3.2.5 on 2021-08-31 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0003_packinglog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packinglog',
            name='totalPacks',
            field=models.IntegerField(default=0),
        ),
    ]
