import re
from django.db.models import fields
from .views import *
from rest_framework import serializers
from Inventory.models import RMReceiving, PMReceiving, PackingMaterials, RawMaterials
from QualityControl.models import RMSamples, PMSamples, ProductSamples
from .utils import getQCNO, PMgetQCNO, FPgetQCNO
from Account.models import User
from .models import *
from datetime import date


#  -------------------- RM SAMPLES --------------------

class GRNOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['GRNo', ]


class RMSampleSerializer(serializers.ModelSerializer):
    GRNo = serializers.IntegerField(write_only=True)

    class Meta:
        model = RMSamples
        fields = ['QCNo', 'GRNo', 'deliveredBy', 'receivedBy', ]

    def create(self, validated_data):
        grno = validated_data['GRNo']
        qcno = getQCNO()
        receiving = RMReceiving.objects.filter(GRNo=grno).first()
        rm = RMSamples.objects.create(
            QCNo=qcno,
            IGPNo=receiving,
            deliveredBy=validated_data['deliveredBy'],
            receivedBy=validated_data['receivedBy']
        )
        rm.save()
        receiving.QCNo = qcno
        receiving.status = 'UNDER_TEST'
        receiving.save()
        return rm


#  -------------------- PM SAMPLES --------------------

class PMGRNOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['GRNo', ]


class PMSampleSerializer(serializers.ModelSerializer):
    GRNo = serializers.IntegerField(write_only=True)

    class Meta:
        model = PMSamples
        fields = ['QCNo', 'GRNo', 'deliveredBy', 'receivedBy', ]

    def create(self, validated_data):
        grno = validated_data['GRNo']
        qcno = PMgetQCNO()
        receiving = PMReceiving.objects.filter(GRNo=grno).first()
        rm = PMSamples.objects.create(
            QCNo=qcno,
            IGPNo=receiving,
            deliveredBy=validated_data['deliveredBy'],
            receivedBy=validated_data['receivedBy']
        )
        rm.save()
        receiving.QCNo = qcno
        receiving.status = 'UNDER_TEST'
        receiving.save()
        return rm


# --------------- NCR ------------------#
class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCCategory
        fields = ['subCategory', ]


class BatchNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo', ]


class NCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = '__all__'

    def create(self, validated_data):
        check = validated_data['isLimitAction']
        if check:
            validated_data['status'] = "CLOSED"
            ncr = NCR.objects.create(**validated_data)
            ncr.closingDate = date.today()
            ncr.save()
        else:
            rootCause = validated_data['rootCause']
            proposedCorrectiveAction = validated_data['proposedCorrectiveAction']
            actionTaken = validated_data['actionTaken']
            if rootCause != "" and proposedCorrectiveAction != "" and actionTaken != "":
                validated_data['status'] = "CLOSED"
            ncr = NCR.objects.create(**validated_data)
        return ncr


#   ---------------- Close NCR    ---------------

class NCRNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = ['NCRNo']


class CloseNCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = ['rootCause', 'proposedCorrectiveAction', 'actionTaken', 'verifiedBy', 'closingDate', ]

    def update(self, instance, validated_data):
        instance.status = 'CLOSED'
        instance.save()
        return super().update(instance, validated_data)


#   ---------------- Close Batch    ---------------


class CloseBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchStatus', 'closingDate']


#   -------------- Add Product -----------------

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class PCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductCode', ]


#   ---------------     View Product    ----------------------

class ProductAndPackSizeSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='ProductCode.Product')
    registrationNo = serializers.CharField(source='ProductCode.RegistrationNo')
    dosageForm = serializers.CharField(source='ProductCode.dosageForm.dosageForm')
    GenericName = serializers.CharField(source='ProductCode.GenericName')
    Composition = serializers.CharField(source='ProductCode.Composition')
    ShelfLife = serializers.CharField(source='ProductCode.ShelfLife')
    RenewalDate = serializers.DateField(source='ProductCode.RenewalDate', format="%d-%m-%Y")

    class Meta:
        model = PackSizes
        fields = ['ProductCode', 'registrationNo', 'PackSize', 'product', 'dosageForm', 'GenericName', 'Composition',
                  'ShelfLife', 'MRP', 'ShelfLife', 'RenewalDate']


# -------------- Add Raw Material -----------------

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = '__all__'


# -------------- Add Packing Material -----------------

class PackingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = '__all__'


# -------------- Batch Deviation ----------------

class BatchDeviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDeviation
        fields = '__all__'


class BatchDeviationNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDeviation
        fields = ['deviationNo', ]


# ---------------- Change Control ---------------
class ChangeControlSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='batchNo.ProductCode.Product')

    class Meta:
        model = ChangeControl
        fields = ['date', 'CCNo','batchNo', 'status', 'initiator', 'department', 'natureOfChange', 'keyword', 'category',
                  'QAStatus', 'name',
                  'descriptionOfChange', 'intendedPurposeOfChange', 'commentsOfProductionManager',
                  'commentsOfQCManager', 'commentsOfPlantDirector', 'commentsOfQAManager','product']    

class ChangeControlForPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChangeControl
        fields = ['status', 'initiator', 'department', 'natureOfChange', 'keyword', 'category',
                  'QAStatus', 'name', 'relatedChanges', 'descriptionOfChange', 'intendedPurposeOfChange', 'commentsOfProductionManager',
                  'commentsOfQCManager', 'commentsOfPlantDirector', 'commentsOfQAManager', 'batchNo','changeDate']


class changeControlVerificationOfChangesSerialerzer(serializers.ModelSerializer):
    class Meta:
        model = ChangeControl
        fields = ['implementedChanges', 'degreeOfImplementation', 'verifiedBy', 'changeDate','status']


# ------------------- DRF  ---------------------#

class DRFItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DRFItems

        fields = ['RMCode', 'formulaQuantity', 'additionalQuantity', ]


class DRFPostSerializer(serializers.ModelSerializer):
    demandedItems = DRFItemsSerializer(many=True, write_only=True)

    class Meta:
        model = DRF
        fields = ['ProductCode', 'BatchNo', 'demandedItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def create(self, validated_data):
        dItems = validated_data.pop('demandedItems')
        drfNo = DRF.objects.create(ProductCode=validated_data.get('ProductCode'), BatchNo=validated_data.get('BatchNo'))
        drfNo.save()

        for i in dItems:
            demands = DRFItems.objects.create(DRFNo=drfNo, RMCode=i['RMCode'],
                                              formulaQuantity=i['formulaQuantity'],
                                              additionalQuantity=i['additionalQuantity'])
            demands.save()
        return drfNo


# ------------------- Product Sample ---------------------#

class ProductSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSamples
        fields = ['batchNo', 'sampleStage', 'sampledBy', 'sampleQuantity', 'sampleUnity']

    def create(self, validated_data):
        qcno = FPgetQCNO()

        prod = ProductSamples.objects.create(
            QCNo=qcno,
            batchNo=validated_data['batchNo'],
            sampleStage=validated_data['sampleStage'],
            sampledBy=validated_data['sampledBy'],
            sampleQuantity=validated_data['sampleQuantity'],
            sampleUnity=validated_data['sampleUnity']
        )
        prod.save()
        return prod


# --------------------- Batch Review ----------------------#

class BatchReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchReview
        fields = '__all__'
