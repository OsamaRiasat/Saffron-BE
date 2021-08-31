from django.db import models
from Products.models import DosageForms, Products
from Planning.models import Plan


# Create your models here.

class Stages(models.Model):
    dosageForm = models.ForeignKey(DosageForms, on_delete=models.CASCADE, related_name="form")
    stage = models.CharField(max_length=20)

    def __str__(self):
        return self.dosageForm.dosageForm


class BatchIssuanceRequest(models.Model):
    planNo = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="plan")
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="pCode")
    noOfBatches = models.IntegerField()

    REQUIRED = ['planNO', 'ProductCode', 'noOfBatches']

    def __str__(self):
        return self.planNo.planNo


class BPRLog(models.Model):
    batchNo = models.CharField(max_length=10, primary_key=True)
    planNo = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="planN")
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="proCode")
    batchSize = models.IntegerField()
    MFGDate = models.DateField()
    EXPDate = models.DateField()

    openingDate = models.DateField(null=True, blank=True)
    closingDate = models.DateField(null=True, blank=True)
    batchStatus = models.CharField(max_length=10, default="OPEN")
    currentStage = models.CharField(max_length=20, default="ISSUED")
    packed = models.IntegerField(default=0)
    inProcess = models.IntegerField(blank=True, null=True)
    yieldPercentage = models.FloatField(blank=True, null=True)

    REQUIRED = ['batchNo', 'planNo', 'ProductCode', 'batchSize', 'MFGDate', 'EXPDate', ]

    def __str__(self):
        return self.batchNo


class BatchStages(models.Model):
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="bNo")
    openingDate = models.DateField()
    closingDate = models.DateField()
    currentStage = models.CharField(max_length=20)
    units = models.CharField(max_length=10)  # kg, g, ml etc
    theoreticalYield = models.IntegerField()
    actualYield = models.IntegerField()
    yieldPercentage = models.FloatField()
    PartialStatus = models.CharField(max_length=10)
    remarks = models.TextField(max_length=100)

    REQUIRED = ['batchNo', 'openingDate', 'closingDate', 'currentStage', 'units', 'theoreticalYield', 'actualYield',
                'yieldPercentage', 'PartialStatus', 'remarks']

    def __str__(self):
        return self.currentStage


class PackingLog(models.Model):
    date = models.DateField(auto_now_add=True)
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="bN")
    packSize = models.CharField(max_length=20)
    noOfPacks = models.IntegerField()  # Qty
    totalPacks = models.IntegerField()  # if there is an existing object to this batchNo
    # than that's object totalPacks = totalPacks + this.totalPacks
    isRepack = models.BooleanField()

    REQUIRED = ['batchNo', 'packSize', 'packSize', 'noOfPacks', 'isRepack']

    def __str__(self):
        return self.batchNo.batchNo
