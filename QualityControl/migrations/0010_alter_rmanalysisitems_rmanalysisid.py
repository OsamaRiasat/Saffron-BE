# Generated by Django 3.2.5 on 2021-08-26 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('QualityControl', '0009_auto_20210826_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rmanalysisitems',
            name='RMAnalysisID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RMAnalysisID_ID', to='QualityControl.rmanalysis'),
        ),
    ]
