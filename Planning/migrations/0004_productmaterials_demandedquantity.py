# Generated by Django 3.2.5 on 2021-08-16 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Planning', '0003_rename_plannedpacks_planitems_packstobeplanned'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmaterials',
            name='demandedQuantity',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
