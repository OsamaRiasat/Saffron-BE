# Generated by Django 3.2.9 on 2022-08-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('QualityControl', '0034_rmsamples_containersreceived'),
    ]

    operations = [
        migrations.AddField(
            model_name='rmsamples',
            name='GRN_No',
            field=models.IntegerField(default=1),
        ),
    ]
