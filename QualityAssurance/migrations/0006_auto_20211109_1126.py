# Generated by Django 3.2.5 on 2021-11-09 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QualityAssurance', '0005_auto_20210907_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='changecontrol',
            name='degreeOfImplementation',
            field=models.CharField(default='ok', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='changecontrol',
            name='implementedChanges',
            field=models.CharField(default='ok', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='changecontrol',
            name='verifiedBy',
            field=models.CharField(default='ok', max_length=50),
            preserve_default=False,
        ),
    ]
