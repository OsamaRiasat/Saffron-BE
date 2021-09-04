import re
from django.db.models import fields
from .views import *
from rest_framework import serializers
from Inventory.models import RMReceiving, PMReceiving
from QualityControl.models import RMSamples, PMSamples
from .utils import getQCNO, PMgetQCNO
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

#--------------- NCR ------------------#
class AllUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]

class SubCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCCategory
        fields = ['subCategory',]

class BatchNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo',]

class NCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = '__all__'
    def create(self, validated_data):
        check = validated_data['isLimitAction']
        if check == True:
            validated_data['status']="CLOSED"
            ncr=NCR.objects.create(**validated_data)
            ncr.closingDate=date.today()
            ncr.save()
        else:
            ncr=NCR.objects.create(**validated_data)
        return ncr

class NCRNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = ['NCRNo']

class CloseNCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = NCR
        fields = ['rootCause','proposedCorrectiveAction','actionTaken','verifiedBy','closingDate',]
    def update(self, instance, validated_data):
        instance.status = 'CLOSED'
        instance.save()
        return super().update(instance, validated_data)