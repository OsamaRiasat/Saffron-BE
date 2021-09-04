import re
from django.db.models import fields
from .views import *
from rest_framework import serializers
from Inventory.models import PackingMaterials, RMReceiving, PMReceiving, RawMaterials
from QualityControl.models import RMSamples, PMSamples
from .utils import getQCNO, PMgetQCNO
from Account.models import User
from .models import *
from datetime import date
from Products.models import Products

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
        qcno = getQCNO()
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

    # def update(self, instance, validated_data):
    #     # instance.batchStatus = 'CLOSED'
    #     # instance.save()
    #     return super().update(instance, validated_data)

#-------------- Add Product -----------------#

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'

class PCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductCode',]

#-------------- Add Raw Material -----------------#

class RawMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = '__all__'

#-------------- Add Packing Material -----------------#

class PackingMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = '__all__'

#-------------- Batch Deviation ----------------#

class BatchDeviationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDeviation
        fields = '__all__'

class BatchDeviationNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchDeviation
        fields = ['deviationNo',]

#---------------- Change Control ---------------#
class ChangeControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeControl
        fields = '__all__'