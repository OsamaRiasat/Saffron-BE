from django.db import models
from Inventory.models import RawMaterials


# Products

class DosageForms(models.Model):
    dosageForm = models.CharField(max_length=20, primary_key=True)  # Tablet, Injection, Capsule etc
    batchSizeUnit = models.CharField(max_length=20, default="units")


class Products(models.Model):
    ProductCode = models.CharField(max_length=10, primary_key=True)
    Product = models.CharField(max_length=30)
    RegistrationNo = models.CharField(max_length=10, unique=True)
    RegistrationDate = models.DateField()
    RenewalDate = models.DateField()
    GenericName = models.CharField(max_length=20)
    Composition = models.CharField(max_length=20)
    ShelfLife = models.DecimalField(max_digits=10, decimal_places=2)
    dosageForm = models.ForeignKey(DosageForms, on_delete=models.CASCADE)

    def __str__(self):
        return self.ProductCode


class PackSizes(models.Model):
    PackSize = models.CharField(max_length=20)  # 1x10, 200ml
    PackType = models.CharField(max_length=20)  # TS, PS
    MRP = models.FloatField()
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.ProductCode.ProductCode +" "+self.PackSize)


class PackSizesListForFrontEnd(models.Model):
    PackSizes = models.CharField(max_length=20)  # To get list of packsizes for front end
    DosageForms = models.ForeignKey(DosageForms, on_delete=models.CASCADE)  # According to this dosage Form

    def __str__(self):
        return self.PackSizes


class Stages(models.Model):
    DosageForms = models.ForeignKey(DosageForms, on_delete=models.CASCADE)  # According to this dosage Form
    stage = models.CharField(max_length=20)

    def __str__(self):
        return self.DosageForms.dosageForm


# Formulation

class Formulation(models.Model):
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    batchSize = models.IntegerField()
    quantity = models.DecimalField(decimal_places=3, max_digits=10)

    date = models.DateField()
    docNo = models.CharField(max_length=10)

    version = models.DecimalField(max_digits=4, decimal_places=1, default=1.0)

    REQUIRED = ['ProductCode', 'RMCode', 'batchSize', 'quantity', 'date', 'docNo']

    def __str__(self):
        return self.ProductCode.Product
