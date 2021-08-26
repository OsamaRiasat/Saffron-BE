from django.db.models import fields
from rest_framework import serializers
from .models import *
from Inventory.models import RawMaterials
from Account.models import User


class RMCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['RMCode', ]


class RMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['Material', ]


class RMReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReferences
        fields = ['reference', ]


class RMParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMParameters
        fields = ['parameter', ]


class RMSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSpecificationsItems
        fields = ['parameter', 'specification', ]


class RMSpecificationsSerializer(serializers.ModelSerializer):
    items = RMSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = RMSpecifications
        fields = ['RMCode', 'reference', 'items']

    def create(self, validated_data):

        try:
            sopno = RMSpecifications.objects.last().SOPNo
        except:
            sopno = "DRL/RMSA/0"

        item = validated_data.pop('items')
        sopno = sopno.split('/')
        no = int(sopno[2])
        no = no + 1
        sopno = sopno[0] + "/" + sopno[1] + "/" + str(no)
        ref = RMReferences.objects.get(reference=validated_data.get('reference'))
        specs = RMSpecifications.objects.create(RMCode=validated_data.get('RMCode'), SOPNo=sopno, reference=ref)
        specs.save()
        for i in item:
            par = RMParameters.objects.get(parameter=i['parameter'])
            itemspecs = RMSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs


class AcquireSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSpecificationsItems
        fields = ['parameter', 'specification', ]


class AcquireRMCodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSpecifications
        fields = ['RMCode', ]


# Edit RM Specs

class TempRMSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempRMSpecificationsItems
        fields = ['parameter', 'specification', ]


class TempRMSpecificationsSerializer(serializers.ModelSerializer):
    items = TempRMSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = TempRMSpecifications
        fields = ['RMCode', 'SOPNo', 'reference', 'version', 'items', ]

    def create(self, validated_data):
        item = validated_data.pop('items')
        specs = TempRMSpecifications.objects.create(**validated_data)
        specs.save()
        for i in item:
            par = RMParameters.objects.get(parameter=i['parameter'])
            itemspecs = TempRMSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs


# RM Sample Assignment
class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', ]


class AssignAnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSamples
        fields = ['analyst', ]


# ---------------- DATA ANALYSIS --------------------

# Raw Materials

class RMAnalysisItemsReportingSerializer(serializers.ModelSerializer):
    material = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.RMCode.Material')
    batchNo = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.batchNo')
    QCNo = serializers.CharField(source='RMAnalysisID.QCNo.QCNo')
    analysisDateTime = serializers.CharField(source='RMAnalysisID.analysisDateTime')

    class Meta:
        model = RMAnalysisItems
        fields = ['material', 'batchNo', 'QCNo', 'analysisDateTime', 'parameter']








# class RMSampleQCNoSerializer
#
# class RMAnalysisItemsReportingSerializer(serializers.ModelSerializer):
#     version = serializers.CharField(source='RMSpecifications.version')
#
#     class Meta:
#         model = RMSpecificationsItems
#         fields = '__all__'
#
#
# class RMSpecificationsItemsForSearchingSerializer(serializers.ModelSerializer):
#     # = RMSpecificationsSerializer(many=True, read_only=True)
#     QAStatus = serializers.CharField(source='specID.QAStatus')
#     RMCode = serializers.CharField(source='specID.RMCode.Material')
#     class Meta:
#         model = RMSpecificationsItems
#         # fields = ['parameter', 'specification', 'specID', 'QAStatus','RMCode']
#         fields = '__all__'
#
# class RMSpecForSearchingSerializer(serializers.ModelSerializer):
#     RMSpecsItems = RMSpecificationsItemsForSearchingSerializer(many=True)
#
#     class Meta:
#         model = RMSpecifications
#         # fields = ['RMSpecsItems', 'version']
#         fields = {
#             'self': ('id', 'parent', 'name'),
#             'parent': ('id', 'label'),
#         }
