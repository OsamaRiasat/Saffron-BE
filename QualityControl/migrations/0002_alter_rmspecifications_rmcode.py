# Generated by Django 3.2.5 on 2021-08-20 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0013_auto_20210812_1218'),
        ('QualityControl', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rmspecifications',
            name='RMCode',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Inventory.rawmaterials'),
        ),
    ]
