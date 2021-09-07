from django.db.models import fields
from rest_framework import serializers
from .models import *
from Planning.models import PlanItems
from rest_framework import serializers


# ------------------Batch Issuance Request--------------------#
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


class BPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['batchNo', 'MFGDate', 'EXPDate', 'currentStage', 'packed', 'inProcess',
                  'yieldPercentage', 'batchStatus']


class PCodeBatchNoBPRSerializer(serializers.ModelSerializer):
    class Meta:
        model = BPRLog
        fields = ['ProductCode', 'batchNo', ]


class BatchStagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BatchStages
        fields = ['batchNo', 'openingDate', 'closingDate', 'currentStage', 'units',
                  'theoreticalYield', 'actualYield', 'yieldPercentage', 'PartialStatus',
                  'remarks']

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


class GeneralDataBPRLogSerializer(serializers.ModelSerializer):
    bNo = BatchStagesSerializer(many=True)

    class Meta:
        model = BPRLog
        fields = ['currentStage', 'ProductCode', 'batchNo', 'batchSize', 'MFGDate', 'EXPDate', 'bNo', ]


# -----------------    Daily Packing      --------------


class PackingLogItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingLog
        fields = ['batchNo', 'packSize', 'noOfPacks', 'isRepack']


class PackingLogSerializer(serializers.ModelSerializer):
    items = PackingLogItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PackingLog
        fields = ['items']

    def create(self, validated_data):
        items = validated_data.get('items')

        for j in items:
            repack = j['isRepack']
            print("repack   ", repack)
            if repack:
                return super().create(j)
            else:
                bno = PackingLog.objects.filter(batchNo=j['batchNo'])
                total = 0
                if bno:
                    for i in bno:
                        if (i.totalPacks > total):
                            total = i.totalPacks
                    pack = PackingLog.objects.create(
                        batchNo=j['batchNo'],
                        packSize=j['packSize'],
                        noOfPacks=j['noOfPacks'],
                        isRepack=j['isRepack'],
                        totalPacks=total + j['noOfPacks'],
                    )
                    pack.save()
                    return pack
                else:
                    pack = PackingLog.objects.create(
                        batchNo=j['batchNo'],
                        packSize=j['packSize'],
                        noOfPacks=j['noOfPacks'],
                        isRepack=j['isRepack'],
                        totalPacks=j['noOfPacks'],
                    )
                    pack.save()
                    return pack


# -----------   Close Order    ------------------

class UpdatePlanItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItems
        fields = ['planNo', 'ProductCode', 'PackSize', 'status']


# --------------- New Formulation For PM -----------------------#

class PMFormulationItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMFormulation

        fields = ['ProductCode', 'PackSize', 'PMCode', 'batchSize', 'quantity', 'date', 'docNo', ]


class PMFormulationSerializer(serializers.ModelSerializer):
    fItems = PMFormulationItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMFormulation
        fields = ['fItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def validate(self, attrs):
        items = attrs.get('fItems')
        code = items[0]['ProductCode']
        ps = items[0]['PackSize']
        check = PMFormulation.objects.filter(ProductCode=code, PackSize=ps)
        if check:
            check.delete()
        return attrs

    def create(self, validated_data):
        items = validated_data.pop('fItems')
        # demand = Formulation.objects.create(**validated_data)
        # demand.save()

        obj = ""
        for i in items:
            item = PMFormulation.objects.create(ProductCode=i['ProductCode'],
                                              PMCode=i['PMCode'],
                                              batchSize=i['batchSize'],
                                              quantity=i['quantity'],
                                              date=i['date'],
                                              PackSize=i['PackSize'],
                                              docNo=i['docNo'])
            item.save()
            obj = i
        return obj

class PMCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode',]

class PMNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['Material',]


class PMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode', 'Material', 'Units', 'Type']

class PackSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackSizes
        fields = ['PackSize',]