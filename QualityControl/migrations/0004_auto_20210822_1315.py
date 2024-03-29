# Generated by Django 3.2.5 on 2021-08-22 08:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Inventory', '0013_auto_20210812_1218'),
        ('QualityControl', '0003_pmparameters_pmspecifications_pmspecificationsitems_productparameters_productspecifications_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='RMSamples',
            fields=[
                ('QCNo', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('deliveredBy', models.CharField(max_length=40)),
                ('receivedBy', models.CharField(max_length=40)),
                ('assignedDateTime', models.DateTimeField(blank=True, null=True)),
                ('analysisDateTime', models.DateTimeField(blank=True, null=True)),
                ('result', models.CharField(blank=True, max_length=20, null=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('remarks', models.CharField(blank=True, max_length=50, null=True)),
                ('IGPNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.rmreceiving')),
                ('analyst', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(

            model_name='rmspecificationsitems',
            name='parameter',
        ),
        migrations.RemoveField(
            model_name='rmspecificationsitems',
            name='reference',
        ),
        migrations.RemoveField(
            model_name='rmspecificationsitems',
            name='specID',
        ),
        migrations.DeleteModel(
            name='RMSpecifications',
        ),
        migrations.DeleteModel(
            name='RMSpecificationsItems',
        ),
    ]
