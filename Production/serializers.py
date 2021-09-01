from django.db.models import fields
from rest_framework import serializers
from rest_framework.views import APIView
from .models import *
from Planning.models import PlanItems
from rest_framework import serializers
from django.db.models import Max

# ------------------Batch Issuence Request--------------------#
class PlanNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItems
        fields = ['planNo']


class PCodeFromPlanItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItems
        fields = ['ProductCode']


class BatchIssuenceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchIssuanceRequest
        fields = '__all__'


class PlanNoBIRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchIssuanceRequest
        fields = ['planNo', ]


class PCodeBIRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchIssuanceRequest
        fields = ['ProductCode', ]


class PlanPCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchIssuanceRequest
        fields = ['planNo', 'ProductCode', ]


class PCodeBatchSizeSerializer(serializers.Serializer):
    Pcode = serializers.CharField()
    batchSize = serializers.IntegerField()


class BPRLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo', 'planNo', 'ProductCode', 'batchSize', 'MFGDate', 'EXPDate', ]


# ----------- Batch Track --------------#
class PCodeBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['ProductCode']


class BatchNoBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo']


class PCodeBatchNoBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['ProductCode', 'batchNo', ]


class BatchStagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStages
        fields = ['batchNo', 'openingDate', 'closingDate', 'currentStage', 'units', 'theoreticalYield', 'actualYield',
                  'yieldPercentage', 'PartialStatus', 'remarks']

    def create(self, validated_data):
        stage = validated_data.get('currentStage')
        bno = validated_data.get('batchNo')
        bpr = BPRLog.objects.get(batchNo=bno)
        bpr.currentStage = stage
        bpr.save()
        return super().create(validated_data)

class DataFromBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo', 'batchSize', 'MFGDate', 'EXPDate', 'currentStage', 'packed', 'inProcess',
                  'yieldPercentage', 'batchStatus', ]

#---------------------- Paking ---------------------------#

class PackingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingLog
        fields = ['batchNo', 'packSize', 'noOfPacks', 'isRepack']

    def create(self, validated_data):
        repack = validated_data.get('isRepack')
        if repack:
            return super().create(validated_data)
        else:
            bno = PackingLog.objects.filter(batchNo=validated_data.get('batchNo'))
            total=0
            if bno:
                for i in bno:
                    if(i.totalPacks>total):
                        total=i.totalPacks
                pack = PackingLog.objects.create(
                    batchNo = validated_data['batchNo'],
                    packSize = validated_data['packSize'],
                    noOfPacks = validated_data['noOfPacks'],
                    isRepack = validated_data['isRepack'],
                    totalPacks = total+validated_data['noOfPacks'],
                )
                pack.save()
                return pack
            else:
                pack = PackingLog.objects.create(
                    batchNo = validated_data['batchNo'],
                    packSize = validated_data['packSize'],
                    noOfPacks = validated_data['noOfPacks'],
                    isRepack = validated_data['isRepack'],
                    totalPacks = validated_data['noOfPacks'],
                )
                pack.save()
                return pack

#----------- Close Order ------------------#
class UpdatePlanItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItems
        fields = ['planNo','ProductCode','PackSize','status']

