from rest_framework import serializers
from .models import *
from Inventory.models import RawMaterials
from Account.models import User
from datetime import date


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     RAW MATERIALS     -----------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

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

    # ------------------ Sample Assignment-------------------


# RM Sample Assignment


class AnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', ]


class AssignAnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSamples
        fields = ['analyst', ]

    def update(self, instance, validated_data):
        instance.analyst = validated_data.get('analyst', instance.analyst)
        instance.assignedDateTime = date.today()
        instance.status = "ASSIGNED"
        instance.save()
        return instance

    class RMAnalysisQCNoSerializer(serializers.ModelSerializer):
        class Meta:
            model = RMAnalysis
            fields = ['QCNo', ]

    # --------------------- Data Entry ------------------------


# RM Data Entry

class RMQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMSamples
        fields = ['QCNo', ]


class PostRMAnalysisItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMAnalysisItems
        fields = ['parameter', 'specification', 'result', ]


class PostRMAnalysisSerializer(serializers.ModelSerializer):
    rm_analysis_items = PostRMAnalysisItemsSerializer(many=True, write_only=True)

    class Meta:
        model = RMAnalysis
        fields = ['QCNo', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate', 'quantityApproved',
                  'quantityRejected', 'remarks', 'rm_analysis_items', ]

    def create(self, validated_data):
        item = validated_data.pop('rm_analysis_items')
        qc = validated_data.get('QCNo')
        print(qc.QCNo)
        RMSample = RMSamples.objects.get(QCNo=qc.QCNo)
        RMSample.status = "TESTED"
        RMSample.save()
        rmcode = RMSamples.objects.get(QCNo=qc.QCNo).IGPNo.RMCode.RMCode
        specID = RMSpecifications.objects.get(RMCode=rmcode).specID
        analysis = RMAnalysis.objects.create(
            QCNo=validated_data['QCNo'],
            specID=specID,
            workingStd=validated_data['workingStd'],
            rawDataReference=validated_data['rawDataReference'],
            analysisDateTime=validated_data['analysisDateTime'],
            retestDate=validated_data['retestDate'],
            quantityApproved=validated_data['quantityApproved'],
            quantityRejected=validated_data['quantityRejected'],
            remarks=validated_data['remarks']

        )
        analysis.save()
        for i in item:
            analysis_items = RMAnalysisItems.objects.create(
                RMAnalysisID=analysis,
                parameter=i['parameter'],
                specification=i['specification'],
                result=i['result']
            )
            analysis_items.save()

        return analysis


# ----------------- COA APPROVAL ------------------#

class RMAnalysisQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMAnalysis
        fields = ['QCNo', ]


class RemarksSerializer(serializers.Serializer):
    remarks = serializers.CharField(default="")
    isRetest = serializers.BooleanField(default=False)
    retestReason = serializers.CharField(default="")
    result = serializers.CharField()

    # ---------------- DATA ANALYSIS --------------------


# Raw Materials
#
# class RMMaterialsListReportingSerializer(serializers.ModelSerializer):
#     material = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.RMCode.Material')
#
#     class Meta:
#         model = RMAnalysisItems
#         fields = ['material', ]
#
#
# class RMBatchNoListReportingSerializer(serializers.ModelSerializer):
#     batchNo = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.batchNo')
#
#     class Meta:
#         model = RMAnalysisItems
#         fields = ['batchNo', ]


class RMAnalysisItemsReportingSerializer(serializers.ModelSerializer):
    material = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.RMCode.Material')
    batchNo = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.batchNo')
    QCNo = serializers.CharField(source='RMAnalysisID.QCNo.QCNo')
    analysisDateTime = serializers.CharField(source='RMAnalysisID.analysisDateTime')
    supplierName = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.S_ID.S_Name')

    class Meta:
        model = RMAnalysisItems
        fields = ['material', 'batchNo', 'QCNo', 'analysisDateTime', 'parameter', 'supplierName']


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PACKING MATERIALS     ---------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class PMCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode', ]


class PMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['Material', ]


#
# class RMReferencesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RMReferences
#         fields = ['reference', ]


class PMParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMParameters
        fields = ['parameter', ]


class PMSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSpecificationsItems
        fields = ['parameter', 'specification', ]


class PMSpecificationsSerializer(serializers.ModelSerializer):
    items = PMSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMSpecifications
        fields = ['PMCode', 'reference', 'items']

    def create(self, validated_data):

        try:
            sopno = PMSpecifications.objects.last().SOPNo
        except:
            sopno = "DRL/PMSA/0"

        item = validated_data.pop('items')
        sopno = sopno.split('/')
        no = int(sopno[2])
        no = no + 1
        sopno = sopno[0] + "/" + sopno[1] + "/" + str(no)
        ref = RMReferences.objects.get(reference=validated_data.get('reference'))
        specs = PMSpecifications.objects.create(PMCode=validated_data.get('PMCode'), SOPNo=sopno, reference=ref)
        specs.save()
        for i in item:
            par = PMParameters.objects.get(parameter=i['parameter'])
            itemspecs = PMSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs


class PMAcquireSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSpecificationsItems
        fields = ['parameter', 'specification', ]


class AcquirePMCodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSpecifications
        fields = ['PMCode', ]


# Edit RM Specs

class TempPMSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempPMSpecificationsItems
        fields = ['parameter', 'specification', ]


class TempPMSpecificationsSerializer(serializers.ModelSerializer):
    items = TempPMSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = TempPMSpecifications
        fields = ['PMCode', 'SOPNo', 'reference', 'version', 'items', ]

    def create(self, validated_data):
        item = validated_data.pop('items')
        specs = TempPMSpecifications.objects.create(**validated_data)
        specs.save()
        for i in item:
            par = PMParameters.objects.get(parameter=i['parameter'])
            itemspecs = TempPMSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs

    # ------------------ Sample Assignment-------------------


# RM Sample Assignment

#
# class AnalystSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', ]
#

class PMAssignAnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSamples
        fields = ['analyst', ]

    def update(self, instance, validated_data):
        instance.analyst = validated_data.get('analyst', instance.analyst)
        instance.assignedDateTime = date.today()
        instance.status = "ASSIGNED"
        instance.save()
        return instance

    class PMAnalysisQCNoSerializer(serializers.ModelSerializer):
        class Meta:
            model = PMAnalysis
            fields = ['QCNo', ]

    # --------------------- Data Entry ------------------------


# PM Data Entry

class PMQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSamples
        fields = ['QCNo', ]


class PostPMAnalysisItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMAnalysisItems
        fields = ['parameter', 'specification', 'result', ]


class PostPMAnalysisSerializer(serializers.ModelSerializer):
    rm_analysis_items = PostPMAnalysisItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMAnalysis
        fields = ['QCNo', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate', 'quantityApproved',
                  'quantityRejected', 'remarks', 'rm_analysis_items', ]

    def create(self, validated_data):
        item = validated_data.pop('rm_analysis_items')
        qc = validated_data.get('QCNo')
        print(qc.QCNo)
        PMSample = PMSamples.objects.get(QCNo=qc.QCNo)
        PMSample.status = "TESTED"
        PMSample.save()
        pmcode = PMSamples.objects.get(QCNo=qc.QCNo).IGPNo.PMCode.PMCode
        specID = PMSpecifications.objects.get(PMCode=pmcode).specID
        analysis = PMAnalysis.objects.create(
            QCNo=validated_data['QCNo'],
            specID=specID,
            workingStd=validated_data['workingStd'],
            rawDataReference=validated_data['rawDataReference'],
            analysisDateTime=validated_data['analysisDateTime'],
            retestDate=validated_data['retestDate'],
            quantityApproved=validated_data['quantityApproved'],
            quantityRejected=validated_data['quantityRejected'],
            remarks=validated_data['remarks']

        )
        analysis.save()
        for i in item:
            analysis_items = PMAnalysisItems.objects.create(
                PMAnalysisID=analysis,
                parameter=i['parameter'],
                specification=i['specification'],
                result=i['result']
            )
            analysis_items.save()

        return analysis


# ----------------- COA APPROVAL ------------------#

class PMAnalysisQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMAnalysis
        fields = ['QCNo', ]


#
# class RemarksSerializer(serializers.Serializer):
#     remarks = serializers.CharField(default="")
#     isRetest = serializers.BooleanField(default=False)
#     retestReason = serializers.CharField(default="")
#     result = serializers.CharField()

# ---------------- DATA ANALYSIS --------------------


# Raw Materials
#
# class PMMaterialsListReportingSerializer(serializers.ModelSerializer):
#     material = serializers.CharField(source='PMAnalysisID.QCNo.IGPNo.PMCode.Material')
#
#     class Meta:
#         model = PMAnalysisItems
#         fields = ['material', ]
#
#
# class PMBatchNoListReportingSerializer(serializers.ModelSerializer):
#     batchNo = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.batchNo')
#
#     class Meta:
#         model = RMAnalysisItems
#         fields = ['batchNo', ]


class PMAnalysisItemsReportingSerializer(serializers.ModelSerializer):
    material = serializers.CharField(source='PMAnalysisID.QCNo.IGPNo.PMCode.Material')
    batchNo = serializers.CharField(source='PMAnalysisID.QCNo.IGPNo.batchNo')
    QCNo = serializers.CharField(source='PMAnalysisID.QCNo.QCNo')
    analysisDateTime = serializers.CharField(source='PMAnalysisID.analysisDateTime')
    supplierName = serializers.CharField(source='PMAnalysisID.QCNo.IGPNo.S_ID.S_Name')

    class Meta:
        model = PMAnalysisItems
        fields = ['material', 'batchNo', 'QCNo', 'analysisDateTime', 'parameter', 'supplierName']

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PRODUCTS     ----------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


class ProductCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductCode', ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['Product', ]


#
# class RMReferencesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RMReferences
#         fields = ['reference', ]


class ProductParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductParameters
        fields = ['parameter', ]


class ProductSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecificationsItems
        fields = ['parameter', 'specification', ]


class ProductSpecificationsSerializer(serializers.ModelSerializer):
    items = ProductSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = ProductSpecifications
        fields = ['ProductCode', 'stage', 'reference', 'items']

    def create(self, validated_data):

        try:
            sopno = ProductSpecifications.objects.last().SOPNo
        except:
            sopno = "DRL/FPSA/0"

        item = validated_data.pop('items')
        sopno = sopno.split('/')
        no = int(sopno[2])
        no = no + 1
        sopno = sopno[0] + "/" + sopno[1] + "/" + str(no)
        ref = RMReferences.objects.get(reference=validated_data.get('reference'))
        specs = ProductSpecifications.objects.create(ProductCode=validated_data.get('ProductCode'),
                                                     SOPNo=sopno,
                                                     reference=ref,
                                                     stage=validated_data.get('stage'))
        specs.save()
        for i in item:
            par = ProductParameters.objects.get(parameter=i['parameter'])
            itemspecs = ProductSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs


class ProductAcquireSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecificationsItems
        fields = ['parameter', 'specification', ]


class AcquireProductCodeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecifications
        fields = ['ProductCode', ]


# Edit RM Specs

class TempProductSpecificationsItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempProductSpecificationsItems
        fields = ['parameter', 'specification', ]


class TempProductSpecificationsSerializer(serializers.ModelSerializer):
    items = TempProductSpecificationsItemsSerializer(many=True, write_only=True)

    class Meta:
        model = TempProductSpecifications
        fields = ['ProductCode','stage', 'SOPNo', 'reference', 'version', 'items', ]

    def create(self, validated_data):
        item = validated_data.pop('items')
        specs = TempProductSpecifications.objects.create(**validated_data)
        specs.save()
        for i in item:
            par = ProductParameters.objects.get(parameter=i['parameter'])
            itemspecs = TempProductSpecificationsItems.objects.create(
                specID=specs,
                parameter=par,
                specification=i['specification']
            )
            itemspecs.save()
        return specs

    # ------------------ Sample Assignment-------------------


# Product Sample Assignment

#
# class AnalystSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', ]
#

class ProductAssignAnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSamples
        fields = ['analyst', ]

    def update(self, instance, validated_data):
        instance.analyst = validated_data.get('analyst', instance.analyst)
        instance.assignedDateTime = date.today()
        instance.status = "ASSIGNED"
        instance.save()
        return instance

    class ProductAnalysisQCNoSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductAnalysis
            fields = ['QCNo', ]

    # --------------------- Data Entry ------------------------


# PM Data Entry

class ProductQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSamples
        fields = ['QCNo', ]


class PostProductAnalysisItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnalysisItems
        fields = ['parameter','specification', 'result' ]


class PostProductAnalysisSerializer(serializers.ModelSerializer):
    product_analysis_items = PostProductAnalysisItemsSerializer(many=True, write_only=True)

    class Meta:
        model = ProductAnalysis
        fields = ['QCNo', 'workingStd', 'rawDataReference', 'analysisDateTime', 'retestDate', 'quantityApproved',
                  'quantityRejected', 'remarks', 'product_analysis_items', ]

    def create(self, validated_data):
        item = validated_data.pop('product_analysis_items')
        qc = validated_data.get('QCNo')
        print(qc.QCNo)
        PMSample = ProductSamples.objects.get(QCNo=qc.QCNo)
        PMSample.status = "TESTED"
        PMSample.save()
        productcode = ProductSamples.objects.get(QCNo=qc.QCNo).batchNo.ProductCode.ProductCode
        specID = ProductSpecifications.objects.get(ProductCode=productcode, stage=qc.sampleStage).specID
        analysis = ProductAnalysis.objects.create(
            QCNo=validated_data['QCNo'],
            specID=specID,
            workingStd=validated_data['workingStd'],
            rawDataReference=validated_data['rawDataReference'],
            analysisDateTime=validated_data['analysisDateTime'],
            retestDate=validated_data['retestDate'],
            quantityApproved=validated_data['quantityApproved'],
            quantityRejected=validated_data['quantityRejected'],
            remarks=validated_data['remarks']

        )
        analysis.save()
        for i in item:
            analysis_items = ProductAnalysisItems.objects.create(
                ProductAnalysisID=analysis,
                parameter=i['parameter'],
                specification=i['specification'],
                result=i['result']
            )
            analysis_items.save()

        return analysis


# ----------------- COA APPROVAL ------------------#

class ProductAnalysisQCNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAnalysis
        fields = ['QCNo', ]


#
# class RemarksSerializer(serializers.Serializer):
#     remarks = serializers.CharField(default="")
#     isRetest = serializers.BooleanField(default=False)
#     retestReason = serializers.CharField(default="")
#     result = serializers.CharField()

# ---------------- DATA ANALYSIS --------------------


# Raw Materials
#
# class PMMaterialsListReportingSerializer(serializers.ModelSerializer):
#     material = serializers.CharField(source='PMAnalysisID.QCNo.IGPNo.PMCode.Material')
#
#     class Meta:
#         model = PMAnalysisItems
#         fields = ['material', ]
#
#
# class PMBatchNoListReportingSerializer(serializers.ModelSerializer):
#     batchNo = serializers.CharField(source='RMAnalysisID.QCNo.IGPNo.batchNo')
#
#     class Meta:
#         model = RMAnalysisItems
#         fields = ['batchNo', ]


class ProductAnalysisItemsReportingSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='ProductMAnalysisID.QCNo.batchNo.ProductCode.Product')
    batchNo = serializers.CharField(source='ProductAnalysisID.QCNo.batchNo.batchNo')
    QCNo = serializers.CharField(source='ProductAnalysisID.QCNo.QCNo')
    analysisDateTime = serializers.CharField(source='ProductAnalysisID.analysisDateTime')
    stage = serializers.CharField(source='ProductAnalysisID.QCNo.sampleStage')

    class Meta:
        model = ProductAnalysisItems
        fields = ['product', 'batchNo', 'QCNo', 'analysisDateTime', 'parameter', 'stage']
