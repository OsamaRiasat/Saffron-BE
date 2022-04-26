from django.db import models


# Create your models here.


# Suppliers

class Suppliers(models.Model):
    S_ID = models.AutoField(primary_key=True)  # 4
    S_Name = models.CharField(max_length=50, unique=True)
    S_Email = models.EmailField()
    S_Address = models.CharField(max_length=50)
    S_City = models.CharField(max_length=50)
    S_Country = models.CharField(max_length=50)
    S_Phone = models.CharField(max_length=50)

    contactPersonName = models.CharField(max_length=50)
    contactPersonPhone = models.CharField(max_length=20)

    def __str__(self):
        return self.S_Name


# zahid@saffronpharama.com

class SupplierApprovedItems(models.Model):
    S_ID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    MCode = models.CharField(max_length=20)
    materialType = models.CharField(max_length=2)
