from django.db import models
from Products.models import Products
from Inventory.models import RawMaterials, PackingMaterials


# Create your models here.


class Plan(models.Model):
    planNo = models.AutoField(primary_key=True)
    date = models.DateField(auto_now_add=True)
    isSaved = models.BooleanField(default=False)
    REQUIRED = ['planNo']


class PlanItems(models.Model):
    planNo = models.ForeignKey(Plan, on_delete=models.CASCADE)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    PackSize = models.CharField(max_length=20)
    requiredPacks = models.DecimalField(decimal_places=3, max_digits=10)
    inHandPacks = models.IntegerField()
    packsToBePlanned = models.IntegerField()
    noOfBatchesToBePlanned = models.DecimalField(max_digits=10, decimal_places=3)
    achievedPacks = models.IntegerField(default=0)
    pendingPacks = models.IntegerField()  # initialise with the required
    status = models.CharField(max_length=10, default="OPEN")

    REQUIRED = ['planNo', 'ProductCode', 'PackSize', 'requiredPacks', 'inHandPacks', 'packsToBePlanned',
                'noOfBatchesToBePlanned']


class ProductMaterials(models.Model):
    planNo = models.ForeignKey(Plan, on_delete=models.CASCADE)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    PackSize = models.CharField(max_length=20)
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    requiredQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    inHandQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    demandedQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    workableBatches = models.DecimalField(max_digits=10, decimal_places=3)

    # def __str__(self):
    #     return self.planNo.planNo

class ProductPackingMaterials(models.Model):
    planNo = models.ForeignKey(Plan, on_delete=models.CASCADE)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    PackSize = models.CharField(max_length=20)
    PMCode = models.ForeignKey(PackingMaterials, on_delete=models.CASCADE)
    requiredQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    inHandQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    demandedQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    workableBatches = models.DecimalField(max_digits=10, decimal_places=3)