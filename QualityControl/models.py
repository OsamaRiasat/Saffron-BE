from decimal import Decimal
from django.db import models
from Inventory.models import RawMaterials, PackingMaterials, PMReceiving
from Production.models import BPRLog
from Products.models import Products
from Inventory.models import RMReceiving
from Account.models import User


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     RAW MATERIALS     -------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# --------------- SPECIFICATIONS --------------------

class RMParameters(models.Model):
    parameter = models.CharField(primary_key=True, max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter


class RMReferences(models.Model):
    reference = models.CharField(primary_key=True, max_length=20)

    REQUIRED = ['reference']

    def __str__(self):
        return self.reference


class RMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    RMCode = models.OneToOneField(RawMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['RMCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.RMCode.RMCode


class RMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(RMParameters, on_delete=models.CASCADE, related_name="items")
    specID = models.ForeignKey(RMSpecifications, on_delete=models.CASCADE, related_name="RMSpecsItems")
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.RMCode.RMCode


class TempRMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    RMCode = models.OneToOneField(RawMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="EDIT")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['RMCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.RMCode.RMCode


class TempRMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(RMParameters, on_delete=models.CASCADE)
    specID = models.ForeignKey(TempRMSpecifications, on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.RMCode.RMCode

    # ------------------ SAMPLE COLLECTION ---------------


# Raw Materials

# QA will make a object (QCNo, IGPNo) of this whenever he takes a sample and also gives that QCNo to RMReceiving
class RMSamples(models.Model):
    # When QA takes sample
    QCNo = models.CharField(max_length=20, primary_key=True)
    IGPNo = models.ForeignKey(RMReceiving, on_delete=models.CASCADE)
    deliveredBy = models.CharField(max_length=40)
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


class RMAnalysis(models.Model):
    RMAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(RMSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField(default=0)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks']

    def __str__(self):
        return self.QCNo.QCNo


class RMAnalysisItems(models.Model):
    RMAnalysisID = models.ForeignKey(RMAnalysis, on_delete=models.CASCADE, related_name='RMAnalysisID_ID')
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['RMAnalysisID', 'parameter', 'specification', 'result']

    def __str__(self):
        return self.RMAnalysisID.QCNo.QCNo


class RMAnalysisLog(models.Model):
    RMAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(RMSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField()
    result = models.CharField(max_length=20)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks', 'specID', 'result']

    def __str__(self):
        return self.QCNo.QCNo


class RMAnalysisItemsLog(models.Model):
    RMAnalysisID = models.ForeignKey(RMAnalysisLog, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['RMAnalysisID', 'parameter', 'specification', 'result']

    def __str__(self):
        return self.RMAnalysisID.QCNo.QCNo


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PACKING MATERIALS     ---------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# --------------- SPECIFICATIONS --------------------


class PMParameters(models.Model):
    parameter = models.CharField(primary_key=True, max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter


class PMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    PMCode = models.OneToOneField(PackingMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['PMCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.PMCode.PMCode


class PMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(PMParameters, on_delete=models.CASCADE, related_name="items")
    specID = models.ForeignKey(PMSpecifications, on_delete=models.CASCADE, related_name="RMSpecsItems")
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.PMCode.PMCode


class TempPMSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    PMCode = models.OneToOneField(PackingMaterials, on_delete=models.CASCADE)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="EDIT")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['PMCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.PMCode.PMCode


class TempPMSpecificationsItems(models.Model):
    parameter = models.ForeignKey(PMParameters, on_delete=models.CASCADE)
    specID = models.ForeignKey(TempPMSpecifications, on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.PMCode.PMCode

    # ------------------ SAMPLE COLLECTION ---------------


# QA will make a object (QCNo, IGPNo) of this whenever he takes a sample and also gives that QCNo to RMReceiving
class PMSamples(models.Model):
    # When QA takes sample
    QCNo = models.CharField(max_length=20, primary_key=True)
    IGPNo = models.ForeignKey(PMReceiving, on_delete=models.CASCADE)
    deliveredBy = models.CharField(max_length=40)
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


class PMAnalysis(models.Model):
    PMAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(PMSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField(default=0)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks']

    def __str__(self):
        return self.QCNo.QCNo


class PMAnalysisItems(models.Model):
    PMAnalysisID = models.ForeignKey(PMAnalysis, on_delete=models.CASCADE, related_name='PMAnalysisID_ID')
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['PMAnalysisID', 'parameter', 'specification', 'result']

    def __str__(self):
        return self.PMAnalysisID.QCNo.QCNo


class PMAnalysisLog(models.Model):
    PMAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(PMSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField()
    result = models.CharField(max_length=20)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks', 'specID', 'result']

    def __str__(self):
        return self.QCNo.QCNo


class PMAnalysisItemsLog(models.Model):
    PMAnalysisID = models.ForeignKey(PMAnalysisLog, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['PMAnalysisID', 'parameter', 'specification', 'result']

    def __str__(self):
        return self.PMAnalysisID.QCNo.QCNo


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PRODUCTS     ------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class ProductParameters(models.Model):
    parameter = models.CharField(primary_key=True, max_length=20)

    REQUIRED = ['parameter']

    def __str__(self):
        return self.parameter


class ProductSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    stage = models.CharField(max_length=30)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="ALLOWED")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['ProductCode', 'stage', 'SOPNo', 'reference']

    def __str__(self):
        return str(self.ProductCode.ProductCode+" "+self.stage)


class ProductSpecificationsItems(models.Model):
    parameter = models.ForeignKey(ProductParameters, on_delete=models.CASCADE, related_name="items")
    specID = models.ForeignKey(ProductSpecifications, on_delete=models.CASCADE, related_name="ProductSpecsItems")
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.ProductCode.ProductCode

class TempProductSpecifications(models.Model):
    specID = models.AutoField(primary_key=True)
    date = models.DateField(auto_now=True)
    ProductCode = models.ForeignKey(Products, on_delete=models.CASCADE)
    stage = models.CharField(max_length=30)
    version = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("1.00"))
    SOPNo = models.CharField(max_length=20, unique=True)
    QAStatus = models.CharField(max_length=10, default="EDIT")  # Change default value to "PENDING" when QA is Done
    reference = models.ForeignKey(RMReferences, on_delete=models.CASCADE)
    REQUIRED = ['ProductCode', 'SOPNo', 'reference']

    def __str__(self):
        return self.ProductCode.ProductCode


class TempProductSpecificationsItems(models.Model):
    parameter = models.ForeignKey(ProductParameters, on_delete=models.CASCADE)
    specID = models.ForeignKey(TempProductSpecifications, on_delete=models.CASCADE)
    specification = models.TextField(max_length=200)

    REQUIRED = ['parameter', 'specID', 'specification']

    def __str__(self):
        return self.specID.ProductCode.ProductCode

#     # ------------------ SAMPLE COLLECTION ---------------


# QA will make a object (QCNo, batchNo, sampleStage) of this whenever he takes
# a sample and also gives that QCNo to RMReceiving
class ProductSamples(models.Model):
    # When QA takes sample
    QCNo = models.CharField(max_length=20, primary_key=True)
    batchNo = models.ForeignKey(BPRLog, on_delete=models.CASCADE)
    sampleStage = models.CharField(max_length=50)
    sampledBy = models.CharField(max_length=40)
    samplingDateTime = models.DateTimeField(auto_now=True)
    sampleQuantity = models.DecimalField(max_digits=10, decimal_places=2)
    sampleUnity = models.CharField(max_length=20)

    # When QC Assigned Samples
    assignedDateTime = models.DateTimeField(blank=True, null=True)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    result = models.CharField(max_length=20, blank=True, null=True)
    analyst = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, default="PENDING")
    remarks = models.CharField(max_length=50, blank=True, null=True)

    REQUIRED = ['QCNo', 'batchNo', 'sampleStage', 'sampledBy', 'sampleQuantity','sampleUnity']


class ProductAnalysis(models.Model):
    ProductAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(ProductSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField(default=0)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks']

    def __str__(self):
        return self.QCNo.QCNo


class ProductAnalysisItems(models.Model):
    ProductAnalysisID = models.ForeignKey(ProductAnalysis, on_delete=models.CASCADE, related_name='ProductAnalysisID_ID')
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['ProductAnalysisID', 'parameter', 'specification', 'result']

    def __str__(self):
        return self.ProductAnalysisID.QCNo.QCNo


class ProductAnalysisLog(models.Model):
    ProductAnalysisID = models.AutoField(primary_key=True)
    workingStd = models.CharField(max_length=40)
    rawDataReference = models.CharField(max_length=40)
    QCNo = models.ForeignKey(ProductSamples, on_delete=models.CASCADE)
    analysisDateTime = models.DateTimeField(blank=True, null=True)
    retestDate = models.DateTimeField(blank=True, null=True)
    quantityApproved = models.DecimalField(max_digits=10, decimal_places=2)
    quantityRejected = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.CharField(max_length=40, blank=True, null=True)
    specID = models.IntegerField()
    result = models.CharField(max_length=20)

    REQUIRED = ['QCNo', 'specID', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate',
                'quantityApproved', 'quantityRejected', 'remarks', 'specID', 'result']

    def __str__(self):
        return self.QCNo.QCNo


class ProductAnalysisItemsLog(models.Model):
    ProductAnalysisID = models.ForeignKey(ProductAnalysisLog, on_delete=models.CASCADE)
    parameter = models.CharField(max_length=20)
    specification = models.TextField(max_length=200)
    result = models.CharField(max_length=20)

    REQUIRED = ['ProductAnalysisID', 'parameter',    'specification', 'result']

    def __str__(self):
        return self.ProductAnalysisID.QCNo.QCNo
