# Generated by Django 3.2.5 on 2021-08-15 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Planning', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='planitems',
            old_name='achieved',
            new_name='achievedPacks',
        ),
        migrations.RenameField(
            model_name='planitems',
            old_name='inHand',
            new_name='inHandPacks',
        ),
        migrations.RenameField(
            model_name='planitems',
            old_name='noOfBatches',
            new_name='noOfBatchesToBePlanned',
        ),
        migrations.RenameField(
            model_name='planitems',
            old_name='pending',
            new_name='pendingPacks',
        ),
        migrations.RenameField(
            model_name='planitems',
            old_name='planned',
            new_name='plannedPacks',
        ),
        migrations.RenameField(
            model_name='planitems',
            old_name='required',
            new_name='requiredPacks',
        ),
    ]
