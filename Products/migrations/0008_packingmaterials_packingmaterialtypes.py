# Generated by Django 3.2.5 on 2021-07-29 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0007_rawmaterials_rawmaterialtypes'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackingMaterialTypes',
            fields=[
                ('Type', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='PackingMaterials',
            fields=[
                ('PMCode', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Material', models.CharField(max_length=50)),
                ('Units', models.CharField(max_length=10)),
                ('Type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.packingmaterialtypes')),
            ],
        ),
    ]
