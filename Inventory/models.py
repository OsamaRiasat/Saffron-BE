from decimal import Decimal

from django.db import models
from MaterialSuppliers.models import Suppliers


# Create your models here.

# Raw Material


class RawMaterialTypes(models.Model):
    Type = models.CharField(max_length=20, primary_key=True)


class RawMaterials(models.Model):
    RMCode = models.CharField(max_length=20, primary_key=True)
    Material = models.CharField(max_length=50)
    Units = models.CharField(max_length=10)
    Type = models.ForeignKey(RawMaterialTypes, on_delete=models.CASCADE)


class RMBinCards(models.Model):
    DateTime = models.DateTimeField(auto_now_add=True)
    particulars = models.CharField(max_length=20, blank=True, null=True)
    batchNo = models.CharField(max_length=20, unique=True)
    received = models.DecimalField(max_digits=10, decimal_places=2)

    issued = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # recieved

    QCNo = models.CharField(max_length=20)
    GRBalance = models.DecimalField(max_digits=10, decimal_places=2)  # received by default
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)


class PackingMaterialTypes(models.Model):
    Type = models.CharField(max_length=20, primary_key=True)


class PackingMaterials(models.Model):
    PMCode = models.CharField(max_length=20, primary_key=True)
    Material = models.CharField(max_length=50)
    Units = models.CharField(max_length=10)
    Type = models.ForeignKey(PackingMaterialTypes, on_delete=models.CASCADE)


class PMBinCards(models.Model):
    DateTime = models.DateTimeField(auto_now_add=True)
    particulars = models.CharField(max_length=20, blank=True, null=True)
    batchNo = models.CharField(max_length=20, unique=True)
    received = models.DecimalField(max_digits=10, decimal_places=2)

    issued = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)  # recieved

    QCNo = models.CharField(max_length=20)
    GRBalance = models.DecimalField(max_digits=10, decimal_places=2)  # received by default
    PMCode = models.ForeignKey(PackingMaterials, on_delete=models.CASCADE)

    # ------------------ DEMANDS -------------------


# Raw Materials


class RMDemands(models.Model):
    DNo = models.BigAutoField(primary_key=True)
    DDate = models.DateTimeField(auto_now_add=True)
    CancelledDate = models.DateTimeField(blank=True, null=True)
    PoNo = models.IntegerField(blank=True, null=True)
    demandStatus = models.CharField(max_length=10, default="PENDING")
    REQUIRED = ['DDate', ]


class RMDemandedItems(models.Model):
    DNo = models.ForeignKey(RMDemands, on_delete=models.CASCADE)
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE, related_name='RCode')
    Priority = models.CharField(max_length=20)
    DemandedQty = models.FloatField(max_length=10)
    CurrentStock = models.FloatField(max_length=10, default=0)
    QuantityPending = models.FloatField(max_length=10, default=0)
    Status = models.CharField(max_length=10, default="Pending")


# Packing Materials


class PMDemands(models.Model):
    DNo = models.BigAutoField(primary_key=True)
    DDate = models.DateTimeField(auto_now_add=True)
    CancelledDate = models.DateTimeField(blank=True, null=True)
    PoNo = models.IntegerField(blank=True, null=True)
    demandStatus = models.CharField(max_length=10, default="PENDING")
    REQUIRED = ['DDate', ]


class PMDemandedItems(models.Model):
    DNo = models.ForeignKey(PMDemands, on_delete=models.CASCADE)
    PMCode = models.ForeignKey(PackingMaterials, on_delete=models.CASCADE, related_name='PCode')
    Priority = models.CharField(max_length=20)
    DemandedQty = models.FloatField(max_length=10)
    CurrentStock = models.FloatField(max_length=10, default=0)
    QuantityPending = models.FloatField(max_length=10, default=0)
    Status = models.CharField(max_length=10, default="Pending")

    # ------------------ PURCHASE ORDERS -------------------


# Raw Materials

class RMPurchaseOrders(models.Model):
    PONo = models.BigAutoField(primary_key=True)
    PODate = models.DateTimeField(auto_now_add=True)
    DNo = models.ForeignKey(RMDemands, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, default="PENDING")
    REQUIRED = ['DNo']


class RMPurchaseOrderItems(models.Model):
    PONo = models.ForeignKey(RMPurchaseOrders, on_delete=models.CASCADE)
    SID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    Quantity = models.FloatField(max_length=10)
    Pending = models.FloatField(max_length=10, blank=True, null=True)
    Received = models.FloatField(max_length=10, default=0)
    Status = models.CharField(max_length=10, default="OPEN")
    CommittedDate = models.DateField(blank=True, null=True)
    Reason = models.CharField(max_length=10, blank=True, null=True)

    REQUIRED = ['PONo', 'SID', 'RMCode', 'Quantity']


# Packing Materials

class PMPurchaseOrders(models.Model):
    PONo = models.BigAutoField(primary_key=True)
    PODate = models.DateTimeField(auto_now_add=True)
    DNo = models.ForeignKey(PMDemands, on_delete=models.CASCADE)
    Status = models.CharField(max_length=10, default="PENDING")
    REQUIRED = ['DNo']


class PMPurchaseOrderItems(models.Model):
    PONo = models.ForeignKey(PMPurchaseOrders, on_delete=models.CASCADE)
    SID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)
    PMCode = models.ForeignKey(PackingMaterials, on_delete=models.CASCADE)
    Quantity = models.FloatField(max_length=10)
    Pending = models.FloatField(max_length=10, blank=True, null=True)
    Received = models.FloatField(max_length=10, default=0)
    Status = models.CharField(max_length=10, default="OPEN")
    CommittedDate = models.DateField(blank=True, null=True)
    Reason = models.CharField(max_length=10, blank=True, null=True)

    REQUIRED = ['PONo', 'SID', 'PMCode', 'Quantity']

    # ------------------ RECEIVING ---------------


# RMReceiving

class RMReceiving(models.Model):
    IGPNo = models.AutoField(primary_key=True)
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    quantityReceived = models.DecimalField(max_digits=10, decimal_places=2)
    containersReceived = models.IntegerField()
    batchNo = models.CharField(max_length=20, unique=True)
    PONo = models.ForeignKey(RMPurchaseOrders, on_delete=models.CASCADE)
    IGPDate = models.DateTimeField(auto_now_add=True)
    S_ID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)

    GRNo = models.IntegerField(default=0)
    MFG_Date = models.DateField(blank=True, null=True)
    EXP_Date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="QUARANTINED")
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    approval_Date = models.DateField(blank=True, null=True)
    QCNo = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.TextField(max_length=100, null=True, blank=True)
    retest_Date = models.DateField(blank=True, null=True)

    REQUIRED = ['RMCode', 'quantityReceived', 'containersReceived', 'batchNo', 'PONo', 'S_ID']


# PMReceiving

class PMReceiving(models.Model):
    IGPNo = models.AutoField(primary_key=True)
    PMCode = models.ForeignKey(PackingMaterials, on_delete=models.CASCADE)
    quantityReceived = models.DecimalField(max_digits=10, decimal_places=2)
    containersReceived = models.IntegerField()
    batchNo = models.CharField(max_length=20, unique=True)
    PONo = models.ForeignKey(PMPurchaseOrders, on_delete=models.CASCADE)
    IGPDate = models.DateTimeField(auto_now_add=True)
    S_ID = models.ForeignKey(Suppliers, on_delete=models.CASCADE)

    GRNo = models.IntegerField(default=0)
    MFG_Date = models.DateField(blank=True, null=True)
    EXP_Date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, default="QUARANTINED")
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    approval_Date = models.DateField(blank=True, null=True)
    QCNo = models.CharField(max_length=20, null=True, blank=True)
    remarks = models.TextField(max_length=100, null=True, blank=True)
    retest_Date = models.DateField(blank=True, null=True)

    REQUIRED = ['PMCode', 'quantityReceived', 'containersReceived', 'batchNo', 'PONo', 'S_ID']
