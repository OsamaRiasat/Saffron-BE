# Generated by Django 3.2.5 on 2021-11-09 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Production', '0008_auto_20210907_1359'),
        ('Inventory', '0018_alter_pmpurchaseorders_dno'),
        ('Products', '0037_alter_packsizes_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='NCCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=30)),
                ('subCategory', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='NCR',
            fields=[
                ('date', models.DateField(auto_now=True)),
                ('NCRNo', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='OPEN', max_length=20)),
                ('originator', models.CharField(max_length=30)),
                ('section', models.CharField(max_length=30)),
                ('sourceOfIdentification', models.CharField(max_length=30)),
                ('refNo', models.CharField(max_length=30)),
                ('natureOfNC', models.CharField(max_length=30)),
                ('gradeOfNC', models.CharField(max_length=30)),
                ('category', models.CharField(max_length=30)),
                ('subCategory', models.CharField(max_length=30)),
                ('descriptionOFNonConformance', models.CharField(max_length=100)),
                ('solutionOfCurrentProblem', models.CharField(max_length=30)),
                ('immediateAction', models.CharField(max_length=30)),
                ('isActionTaken', models.BooleanField()),
                ('actionDate', models.DateField(blank=True, null=True)),
                ('closingDate', models.DateField(blank=True, null=True)),
                ('verifiedBy', models.CharField(max_length=30)),
                ('isLimitAction', models.BooleanField()),
                ('rootCause', models.CharField(blank=True, max_length=100, null=True)),
                ('proposedCorrectiveAction', models.CharField(blank=True, max_length=100, null=True)),
                ('actionTaken', models.CharField(blank=True, max_length=100, null=True)),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BN', to='Production.bprlog')),
            ],
        ),
        migrations.CreateModel(
            name='DRFItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formulaQuantity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('additionalQuantity', models.DecimalField(decimal_places=3, max_digits=10)),
                ('RMCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DRFItem', to='Inventory.rawmaterials')),
            ],
        ),
        migrations.CreateModel(
            name='DRF',
            fields=[
                ('DRFNo', models.AutoField(primary_key=True, serialize=False)),
                ('Date', models.DateField(auto_now=True)),
                ('BatchNo', models.CharField(max_length=20)),
                ('ProductCode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drf', to='Products.products')),
            ],
        ),
        migrations.CreateModel(
            name='ChangeControl',
            fields=[
                ('date', models.DateField(auto_now=True)),
                ('CCNo', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(default='OPEN', max_length=20)),
                ('initiator', models.CharField(max_length=30)),
                ('department', models.CharField(max_length=30)),
                ('natureOfChange', models.CharField(max_length=30)),
                ('keyword', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('QAStatus', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30)),
                ('relatedChanges', models.CharField(max_length=200)),
                ('descriptionOfChange', models.CharField(max_length=200)),
                ('intendedPurposeOfChange', models.CharField(max_length=200)),
                ('commentsOfProductionManager', models.CharField(blank=True, max_length=200, null=True)),
                ('commentsOfQCManager', models.CharField(blank=True, max_length=200, null=True)),
                ('commentsOfPlantDirector', models.CharField(max_length=200)),
                ('commentsOfQAManager', models.CharField(max_length=200)),
                ('implementedChanges', models.CharField(max_length=500)),
                ('degreeOfImplementation', models.CharField(max_length=500)),
                ('verifiedBy', models.CharField(max_length=50)),
                ('changeDate', models.DateField()),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BR', to='Production.bprlog')),
            ],
        ),
        migrations.CreateModel(
            name='BatchReview',
            fields=[
                ('date', models.DateField(auto_now=True)),
                ('BRNo', models.AutoField(primary_key=True, serialize=False)),
                ('dispatchPermission', models.CharField(max_length=30)),
                ('permittedDispatch', models.CharField(max_length=30)),
                ('remarks', models.CharField(blank=True, max_length=200, null=True)),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BRNo', to='Production.bprlog')),
            ],
        ),
        migrations.CreateModel(
            name='BatchDeviation',
            fields=[
                ('date', models.DateField(auto_now=True)),
                ('deviationNo', models.AutoField(primary_key=True, serialize=False)),
                ('stage', models.CharField(max_length=50)),
                ('keyword', models.CharField(max_length=30)),
                ('descriptionOfDeviation', models.CharField(blank=True, max_length=200, null=True)),
                ('actionTaken', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(default='CLOSED', max_length=20)),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='BDNo', to='Production.bprlog')),
            ],
        ),
    ]
