from decimal import Decimal
from django.db import models
from Inventory.models import RawMaterials, PackingMaterials
from Products.models import Products
from Inventory.models import RMReceiving
from Account.models import User
# Create your models here.


    # --------------- SPECIFICATIONS --------------------

# Raw Materials

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
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['RMCode','SOPNo','reference']

    def __str__(self):
        return self.RMCode.RMCode

class RMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(RMParameters, on_delete=models.CASCADE)
    specID = models.ForeignKey(RMSpecifications,related_name='items', on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED  = ['parameter','specID','specification']

    def __str__(self):
        return self.specID.RMCode.RMCode

class TempRMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    RMCode = models.OneToOneField(RawMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10,default="EDIT")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['RMCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.RMCode.RMCode

class TempRMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(RMParameters, on_delete=models.CASCADE)
    specID = models.ForeignKey(TempRMSpecifications,related_name='items', on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.RMCode.RMCode




# Packing Materials

class PMParameters(models.Model):
    parameter = models.CharField(primary_key=True,max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter

class PMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    PMCode = models.OneToOneField(PackingMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED") # Change default value to "PENDING" when QA is Done

    REQUIRED = ['PMCode','SOPNo']

    def __str__(self):
        return self.PMCode.PMCode

class PMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(PMParameters, on_delete=models.CASCADE)
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    specID = models.ForeignKey(PMSpecifications, on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED  = ['parameter','reference','specID','specification']

    def __str__(self):
        return self.specID.PMCode.PMCode


# Products

class ProductParameters(models.Model):
    parameter = models.CharField(primary_key=True,max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter

class ProductSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    stage = models.CharField(max_length=20)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED") # Change default value to "PENDING" when QA is Done

    REQUIRED = ['ProductCode','SOPNo']

    def __str__(self):
        return self.ProductCode.ProductCode

class ProductSpecificationsItems(models.Model):
    parameter = models.ForeignKey(ProductParameters, on_delete=models.CASCADE)
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    specID = models.ForeignKey(ProductSpecifications, on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED  = ['parameter','reference','specID','specification']

    def __str__(self):
        return self.specID.ProductCode.ProductCode


    # ------------------ SAMPLE COLLECTION ---------------

# Raw Materials

# QA will make a object (QCNo, IGPNo) of this whenever he takes a sample and also gives that QCNo to RMReceiving
class RMSamples(models.Model):
    # When QA takes sample
    QCNo = models.CharField(max_length=20,primary_key=True)
    IGPNo = models.ForeignKey(RMReceiving,related_name='rmsamples', on_delete=models.CASCADE)
    deliveredBy = models.CharField(max_length=40 )
    receivedBy = models.CharField(max_length=40)
    samplingDateTime = models.DateTimeField(auto_now=True)

    # When QC Assigned Samples
    assignedDateTime = models.DateTimeField(blank=True, null=True)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, null=True)
    analyst = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    remarks = models.CharField(max_length=50, blank=True, null=True)

    REQUIRED = ['QCNo', 'IGPNo', 'deliveredBy', 'receivedBy']
#
# class RMAnalysis(models.Model):
#     RMAnalysisID = models.AutoField(primary_key=True)
#     workingStd = models.CharField(max_length=40)
#     QCNo = models.ForeignKey(RMSamples, on_delete=models.CASCADE)
#     analysisDateTime = models.DateTimeField(blank=True, null=True)
#     retestDate = models.DateTimeField(blank=True, null=True)
#     quantityApproved  = models.DecimalField(max_digits=10, decimal_places=2)
#     quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
#     remarks = models.CharField(max_length=40 , blank=True, null=True )
#
#     REQUIRED = ['QCNo', 'workingStd', 'analysisDateTime', 'retestDate', 'quantityApproved', 'quantityRejected', 'remarks']
#
# class RMAnalysisItems(models.Model):
#     RMAnalysisID = models.ForeignKey(RMAnalysis, on_delete=models.CASCADE)
#     parameter = models.CharField( max_length=20)
#     specification = models.TextField(max_length=200)
#     result = models.CharField( max_length=20)
#
#     REQUIRED = ['RMAnalysisID', 'parameter' , 'specification', 'result']
