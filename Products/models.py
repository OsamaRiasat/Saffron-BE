from django.db import models


# Products

class DosageForms(models.Model):
    dosageForm = models.CharField(max_length=20, primary_key=True)  # Tablet, Injection, Capsule etc


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
        return self.Product


class PackSizes(models.Model):
    PackSize = models.CharField(max_length=20)  # 1x10, 200ml
    PackType = models.CharField(max_length=20, unique=True)  # TS, PS
    MRP = models.FloatField()
    RegistrationNo = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return self.RegistrationNo.Product


class PackSizesListForFrontEnd(models.Model):
    PackSizes = models.CharField(max_length=20)  # To get list of packsizes for front end
    DosageForms = models.ForeignKey(DosageForms, on_delete=models.CASCADE)  # According to this dosage Form

    def __str__(self):
        return self.PackSizes
