# Generated by Django 3.2.9 on 2021-12-17 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Production', '0008_auto_20210907_1359'),
    ]

    operations = [
        migrations.CreateModel(
            name='FGStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateTime', models.DateTimeField(auto_now_add=True)),
                ('particulars', models.CharField(blank=True, max_length=20, null=True)),
                ('PackSize', models.CharField(max_length=20)),
                ('received', models.DecimalField(decimal_places=2, max_digits=10)),
                ('issued', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('QCNo', models.CharField(max_length=20)),
                ('batchNo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Production.bprlog')),
            ],
        ),
    ]
