from decimal import Decimal
from django.db import models
from Inventory.models import RawMaterials

# Create your models here.


# SPECIFICATIONS FOR Raw Materials

class RMParameters(models.Model):
    parameter = models.CharField(primary_key=True,max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter

class RMReferences(models.Model):
    reference = models.CharField(primary_key=True,max_length=20)

    REQUIRED = ['reference']

    def __str__(self):
        return self.reference

class RMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    RMCode = models.OneToOneField(RawMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED") # Change default value to "PENDING" when QA is Done

    REQUIRED = ['RMCode','SOPNo']

    def __str__(self):
        return self.RMCode.RMCode

class RMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(RMParameters, on_delete=models.CASCADE)
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    specID = models.ForeignKey(RMSpecifications,related_name='items', on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED  = ['parameter','reference','specID','specification']

    def __str__(self):
        return self.specID.RMCode.RMCode


    