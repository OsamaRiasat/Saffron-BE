# Generated by Django 3.2.9 on 2022-08-08 17:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QualityControl', '0027_auto_20220808_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rmsamples',
            name='EXP_Date',
        ),
        migrations.RemoveField(
            model_name='rmsamples',
            name='MFG_Date',
        ),
        migrations.RemoveField(
            model_name='rmsamples',
            name='RMCode',
        ),
        migrations.RemoveField(
            model_name='rmsamples',
            name='S_ID',
        ),
        migrations.RemoveField(
            model_name='rmsamples',
            name='batchNo',
        ),
        migrations.RemoveField(
            model_name='rmsamples',
            name='quantityReceived',
        ),
    ]
