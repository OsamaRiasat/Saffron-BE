from django.db import models



# Products

class Products(models.Model):
    ProductCode = models.CharField(max_length=5)
    Product = models.CharField(max_length=30, unique=True, default='No Name')
    RegistrationNo = models.CharField(max_length=10, primary_key=True)
    RegistrationDate = models.DateField()
    RenewalDate = models.DateField()
    DosageForm = models.CharField(max_length=20)
    GenericName = models.CharField(max_length=20)
    Composition = models.CharField(max_length=20)
    ShelfLife = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.RegistrationNo


class DosageForms(models.Model):
    PackSize = models.CharField(primary_key=True, max_length=20)
    PackType = models.CharField(max_length=20, unique=True)
    Type = models.CharField(max_length=20)


class PackSizes(models.Model):
    PackSize = models.ForeignKey(DosageForms, on_delete=models.CASCADE)
    MRP = models.FloatField()
    RegistrationNo = models.ForeignKey(Products, on_delete=models.CASCADE)


