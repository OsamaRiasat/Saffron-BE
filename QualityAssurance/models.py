from django.db import models

# Create your models here.
from Inventory.models import RawMaterials
from Production.models import BPRLog
from Products.models import Products


#   ------------------ Non Conformance  ------------------


class NCCategory(models.Model):
    category = models.CharField(max_length=30)
    subCategory = models.CharField(max_length=30)

    REQUIRED = ['category', 'subCategory']

    def __str__(self):
        return str(self.category)


class NCR(models.Model):
    date = models.DateField(auto_now=True)
    NCRNo = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, default="OPEN")
    originator = models.CharField(max_length=30)
    section = models.CharField(max_length=30)
    sourceOfIdentification = models.CharField(max_length=30)
    refNo = models.CharField(max_length=30)
    natureOfNC = models.CharField(max_length=30)
    gradeOfNC = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    subCategory = models.CharField(max_length=30)
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="BN")
    descriptionOFNonConformance = models.CharField(max_length=100)
    solutionOfCurrentProblem = models.CharField(max_length=30)
    immediateAction = models.CharField(max_length=30)
    isActionTaken = models.BooleanField()
    actionDate = models.DateField(null=True, blank=True)
    closingDate = models.DateField(null=True, blank=True)
    verifiedBy = models.CharField(max_length=30)
    isLimitAction = models.BooleanField()
    rootCause = models.CharField(max_length=100, null=True, blank=True)
    proposedCorrectiveAction = models.CharField(max_length=100, null=True, blank=True)
    actionTaken = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.NCRNo)


class BatchDeviation(models.Model):
    date = models.DateField(auto_now=True)
    deviationNo = models.AutoField(primary_key=True)
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="BDNo")
    stage = models.CharField(max_length=50)
    keyword = models.CharField(max_length=30)
    descriptionOfDeviation = models.CharField(max_length=200, null=True, blank=True)
    actionTaken = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default="CLOSED")

    def __str__(self):
        return str(self.deviationNo)


class ChangeControl(models.Model):

    date = models.DateField(auto_now=True)
    CCNo = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, default="OPEN")
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="BR")
    initiator = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    natureOfChange = models.CharField(max_length=30)
    keyword = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    QAStatus = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    relatedChanges = models.CharField(max_length=200)
    descriptionOfChange = models.CharField(max_length=200)
    intendedPurposeOfChange = models.CharField(max_length=200)
    commentsOfProductionManager = models.CharField(max_length=200, blank=True, null=True)
    commentsOfQCManager = models.CharField(max_length=200, blank=True, null=True)
    commentsOfPlantDirector = models.CharField(max_length=200)
    commentsOfQAManager = models.CharField(max_length=200)

    implementedChanges = models.CharField(max_length=500)
    degreeOfImplementation = models.CharField(max_length=500)
    verifiedBy = models.CharField(max_length=50)
    changeDate = models.DateField()

    def __str__(self):
        return str(self.CCNo)

    #   --------------------  Dispensation Request Form  -------------------


class DRF(models.Model):
    DRFNo = models.AutoField(primary_key=True)
    Date = models.DateField(auto_now=True)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='drf')
    BatchNo = models.CharField(max_length=20)

    REQUIRED = ['DRFNo', 'ProductCode', 'BatchNo']

    def __str__(self):
        return self.BatchNo


class DRFItems(models.Model):
    DRFNo = models.ForeignKey(DRF,on_delete=models.CASCADE, related_name='drf')
    RMCode = models.ForeignKey(RawMaterials, on_delete=models.CASCADE)
    formulaQuantity = models.DecimalField(decimal_places=3, max_digits=10)
    additionalQuantity = models.DecimalField(decimal_places=3, max_digits=10)
    REQUIRED = ['RMCode', 'formulaQuantity', 'additionalQuantity']

    def __str__(self):
        return self.RMCode.RMCode

    #   --------------------  Batch review  -------------------


class BatchReview(models.Model):
    date = models.DateField(auto_now=True)
    BRNo = models.AutoField(primary_key=True)
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE, related_name="BRNo")
    dispatchPermission = models.CharField(max_length=30)
    permittedDispatch = models.CharField(max_length=30)
    remarks = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.BRNo

# class FGBinCards(models.Model):
#     DateTime = models.DateTimeField(auto_now_add=True)
#     ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE, related_name="FG")
#     packSize = models.CharField(max_length=20)
