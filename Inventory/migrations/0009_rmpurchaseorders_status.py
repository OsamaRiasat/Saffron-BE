# Generated by Django 3.2.5 on 2021-08-05 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0008_rmbincards'),
    ]

    operations = [
        migrations.AddField(
            model_name='rmpurchaseorders',
            name='Status',
            field=models.CharField(default='PENDING', max_length=10),
        ),
    ]
