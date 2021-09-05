import re

from Products.models import Formulation, PackSizes
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from Planning.models import *
from .serializers import *
from datetime import date
from dateutil.relativedelta import relativedelta
from .utils import CreateBatchNo, getStandardBatchSize
from Products.serializers import (
    PCodeSerializer,
    PNameSerializer,
)
from Products.utils import getCode, getName

# Create your views here.

# ------------------Batch Issuence Request--------------------#
class PlanNoView(APIView):
    def get(self, request):
        plans = PlanItems.objects.filter(status='OPEN').values_list('planNo').distinct()
        entries = PlanItems.objects.filter(id__in=plans)
        serializer = PlanNoSerializer(entries, many=True)
        return Response(serializer.data)


class ProductByPlanNoView(APIView):  # retrieve only distinct
    def get(self, request, planNo):
        product = PlanItems.objects.filter(planNo=planNo).values_list('ProductCode').distinct()
        dict = []
        for i in product:
            dic = {}
            dic['ProductCode'] = i[0]
            dict.append(dic)
        return Response(dict)


class SBSView(APIView):
    def get(self, request, PCode):
        size = getStandardBatchSize(PCode)
        return Response({'Units': size})


class BatchIssuenceRequestView(generics.CreateAPIView):
    queryset = BatchIssuanceRequest.objects.all()
    serializer_class = BatchIssuenceRequestSerializer


class PlanNoBIRView(APIView):
    def get(self, request):
        plans = BatchIssuanceRequest.objects.filter(noOfBatches__gt=0).values_list('planNo').distinct()
        entries = BatchIssuanceRequest.objects.filter(planNo__in=plans)
        serializer = PlanNoBIRSerializer(entries, many=True)
        return Response(serializer.data)


class PCodeBIRView(APIView):
    def get(self, request, planNo):
        plans = BatchIssuanceRequest.objects.filter(planNo=planNo).values_list('ProductCode').distinct()
        entries = BatchIssuanceRequest.objects.filter(ProductCode__in=plans)
        serializer = PCodeBIRSerializer(entries, many=True)
        return Response(serializer.data)


class IssueBatchNoView(APIView):
    serializer_class = PlanPCodeSerializer

    def post(self, request):
        data = request.data
        planNo = data.get('planNo', None)
        Pcode = data.get('ProductCode', None)
        product = Products.objects.get(ProductCode=Pcode)
        dict = {}
        dict['Date'] = date.today()
        dict['planNo'] = planNo
        dict['Product'] = product.Product
        dict['Dosage'] = product.dosageForm.dosageForm
        dict['batchSize'] = getStandardBatchSize(Pcode)
        dict['MFG_Date'] = date.today().strftime("%d.%m.%Y")
        shelf_life = Products.objects.get(ProductCode=Pcode).ShelfLife
        dict['EXP_Date'] = (date.today() + relativedelta(years=+shelf_life)).strftime("%d.%m.%Y")
        batchNo = CreateBatchNo(Pcode)
        dict['batchNo'] = batchNo
        return Response(dict)


class FormulationView(APIView):
    serializer_class = PCodeBatchSizeSerializer

    def post(self, request):
        data = request.data
        batch_size = data.get('batchSize', None)
        Pcode = data.get('Pcode', None)
        sbs = getStandardBatchSize(Pcode)
        total = batch_size / sbs
        formulation = Formulation.objects.filter(ProductCode=Pcode)
        dict = []
        for i in formulation:
            dic = {}
            dic['Type'] = i.RMCode.Type.Type
            dic['RMCode'] = i.RMCode.RMCode
            dic['Material'] = i.RMCode.Material
            dic['Units'] = i.RMCode.Units
            dic['Quantity'] = round(float(i.quantity) * float(total), 3)
            dict.append(dic)
        return Response(dict)


class BPRLogView(generics.CreateAPIView):
    queryset = BPRLog.objects.all()
    serializer_class = BPRLogSerializer


# ----------- Batch Track --------------#

class PCodeBPRView(APIView):
    def get(self, request):
        pcode = BPRLog.objects.filter(batchStatus='OPEN').values_list('ProductCode').distinct()
        entries = BPRLog.objects.filter(ProductCode__in=pcode)
        serializer = PCodeBPRSerializer(entries, many=True)
        return Response(serializer.data)


class BPRByPcodeView(APIView):
    def get(self, request, PCode):
        batchNo = BPRLog.objects.filter(ProductCode=PCode)
        serializer = BPRSerializer(batchNo, many=True)
        return Response(serializer.data)


class GeneralDataBPRLogView(APIView):
    serializer_class = PCodeBatchNoBPRSerializer

    def post(self, request):
        data = request.data
        pcode = data.get('ProductCode', None)
        batchNo = data.get('batchNo', None)
        gdata = BPRLog.objects.get(ProductCode=pcode, batchNo=batchNo)
        dict = {}
        dict['currentStage'] = gdata.currentStage
        dict['ProductCode'] = pcode
        dict['batchNo'] = batchNo
        dict['batchSize'] = gdata.batchSize
        dict['MFGDate'] = gdata.MFGDate
        dict['EXPDate'] = gdata.EXPDate
        li = []
        stages = BatchStages.objects.filter(batchNo=batchNo)
        for i in stages:
            dic = {}
            dic['currentStage'] = i.currentStage
            dic['openingDate'] = i.openingDate
            dic['closingDate'] = i.closingDate
            dic['units'] = i.units
            dic['theoreticalYield'] = i.theoreticalYield
            dic['actualYield'] = i.actualYield
            dic['yieldPercentage'] = i.yieldPercentage
            dic['PartialStatus'] = i.PartialStatus
            li.append(dic)
        dict['ListToBeAddedInTable'] = li

        data = Stages.objects.filter(dosageForm=gdata.ProductCode.dosageForm)
        l = []
        for i in data:
            l.append(i.stage)
        dict['ListOfStages'] = l

        return Response(dict)


class BatchStagesView(generics.CreateAPIView):
    queryset = BatchStages.objects.all()
    serializer_class = BatchStagesSerializer


class DataFromBPRView(APIView):
    def get(self, request, PCode):
        data = BPRLog.objects.filter(ProductCode=PCode, batchStatus='OPEN')
        serializer = DataFromBPRSerializer(data, many=True)
        return Response(serializer.data)


# -----------------    Daily Packing      --------------


class WhenProductIsSelectedView(APIView):
    def get(self, request, PCode):
        product = PlanItems.objects.filter(ProductCode=PCode)
        dosage = Products.objects.get(ProductCode=PCode).dosageForm
        print(product)
        dict = {}
        dict['DosageForm'] = dosage.dosageForm
        li = []
        for i in product:
            dic = {}
            dic['PackSize'] = i.PackSize
            li.append(dic)
        dict['PackSizes'] = li

        bno = BPRLog.objects.filter(ProductCode=PCode, currentStage='Packing')
        serializer = BatchNoBPRSerializer(bno, many=True)
        dict['batchNosList'] = serializer.data
        return Response(dict)


class PackingLogView(generics.CreateAPIView):
    queryset = PackingLog.objects.all()
    serializer_class = PackingLogSerializer


# -----------------    Line Clearance      --------------


class PCodesForLineClearanceView(APIView):
    def get(self, request):
        # pcode = BPRLog.objects.distinct().filter(batchStatus='OPEN').values_list('ProductCode').distinct()
        # entries = BPRLog.objects.filter(ProductCode__in=pcode).values('ProductCode').distinct()
        # serializer = PCodeBPRSerializer(entries, many=True)

        l = []
        d = BPRLog.objects.only('ProductCode').filter(batchStatus='OPEN').distinct()
        for i in d:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        return Response(l)


class BatchNoBYPCodeView(APIView):
    def get(self, request, PCode):
        bno = BPRLog.objects.filter(ProductCode=PCode).only('batchNo')
        serializer = BatchNoBPRSerializer(bno, many=True)
        return Response(serializer.data)


class WhenBatchNoIsSelectedView(APIView):
    def get(self, request, batchNo):
        dic = {}

        BPR = BPRLog.objects.get(batchNo=batchNo)
        dic["currentStage"] = BPR.currentStage
        dic["product"] = BPR.ProductCode.Product
        dic["batchNo"] = BPR.batchNo
        dic["batchSize"] = BPR.batchSize
        dic["mfgDate"] = BPR.MFGDate
        dic["expDate"] = BPR.EXPDate

        batchStages = BatchStages.objects.filter(batchNo=batchNo)
        l = []
        for stage in batchStages:
            d = {}
            d["stage"] = stage.currentStage
            d["startDate"] = stage.openingDate
            d["completion"] = stage.closingDate
            d["yieldPercentage"] = stage.yieldPercentage
            d["stageStatus"] = stage.PartialStatus
            l.append(d)

        dic["stagesList"] = l

        return Response(dic)


# -------------      Close Order     ----------------

class PlanItemsView(APIView):
    def get(self, request):
        plans = PlanItems.objects.filter(status='OPEN')
        dict = []
        for i in plans:
            dic = {}
            dic['planNo'] = i.planNo.planNo
            dic['ProductCode'] = i.ProductCode.ProductCode
            dic['Product'] = i.ProductCode.Product
            dic['PackSize'] = i.PackSize
            dic['requiredPacks'] = i.requiredPacks
            dic['achievedPacks'] = i.achievedPacks
            dic['pendingPacks'] = i.pendingPacks
            dic['status'] = i.status
            dic['date'] = i.planNo.date.strftime("%d.%m.%Y")
            dict.append(dic)
        return Response(dict)


class PlanStatusView(APIView):
    serializer_class = UpdatePlanItemsSerializer

    def put(self, request):
        data = request.data
        planNo = data.get('planNo', None)
        ProductCode = data.get('ProductCode', None)
        PackSize = data.get('PackSize', None)
        Status = data.get('status', None)
        plan = PlanItems.objects.get(planNo=planNo, ProductCode=ProductCode, PackSize=PackSize)
        plan.status = Status
        plan.save()
        return Response()


#   ------------------------- Raw Material Assessment ---------------------

class ListOfPCodeForAssessmentView(APIView):
    def get(self, request):
        data = Formulation.objects.only('ProductCode').all()
        l = []

        for i in data:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        return Response({"List": l})


class ListOfPNameForAssessmentView(APIView):
    def get(self, request):
        data = Formulation.objects.only('ProductCode').all()
        l = []

        for i in data:
            l.append(i.ProductCode.Product)
        l = list(dict.fromkeys(l))
        return Response({"List": l})


class PCodeByPNameAssessmentView(APIView):
    def get(self, request, PName):
        try:
            data = Products.objects.only('ProductCode').get(Product=PName)
        except:
            return Response({"message": "No Product Name Against this Code"})

        return Response({"PCode": data.ProductCode})


class PackSizesListView(APIView):
    def get(self, request, PCode):
        data = PackSizes.objects.filter(ProductCode=PCode)
        l = []
        for i in data:
            l.append(i.PackSize)

        sbs = getStandardBatchSize(PCode)
        productName = Products.objects.only('ProductCode').get(ProductCode=PCode)
        return Response({"list": l, "batchSize": sbs, "productName": productName.Product})


class ViewFormulationForAssessmentView(APIView):
    def get(self, request, Pcode, batch_size, noOfBatches):
        noOfBatches = float(noOfBatches)
        batch_size = float(batch_size)
        sbs = getStandardBatchSize(Pcode)
        total = (batch_size / sbs) * noOfBatches
        formulation = Formulation.objects.filter(ProductCode=Pcode)
        dict = []
        for i in formulation:
            dic = {}
            dic['Type'] = i.RMCode.Type.Type
            dic['RMCode'] = i.RMCode.RMCode
            dic['Material'] = i.RMCode.Material
            dic['Units'] = i.RMCode.Units
            dic['Quantity'] = round(float(i.quantity) * float(total), 3)
            dict.append(dic)
        return Response(dict)


# ----------------------New Formulation For PM----------------------#

class PCodeView(APIView):
    def get(self, request):
        li = PMFormulation.objects.values_list('ProductCode')
        pcode = Products.objects.exclude(ProductCode__in=li)
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class PNameView(APIView):
    def get(self, request):
        li = PMFormulation.objects.values_list('ProductCode')
        pcode = Products.objects.exclude(ProductCode__in=li)
        serializer = PNameSerializer(pcode, many=True)
        return Response(serializer.data)


class PCodeByPnameView(APIView):
    def get(self, request, Product):
        code = getCode(Product)
        return Response(code)


class PnameByPCodeView(APIView):
    def get(self, request, Pcode):
        name = getName(Pcode)
        return Response(name)


class PMCodeView(APIView):
    def get(self, request):
        rmcode = PackingMaterials.objects.all()
        serializer = PMCodeSerializer(rmcode, many=True)
        return Response(serializer.data)


class PMNameView(APIView):
    def get(self, request):
        rmcode = PackingMaterials.objects.all()
        serializer = PMNameSerializer(rmcode, many=True)
        return Response(serializer.data)


class PMCodeByNameView(APIView):
    def get(self, request, PMName):
        rmcode = PackingMaterials.objects.get(Material=PMName)
        serializer = PMCodeSerializer(rmcode)
        return Response(serializer.data)


class PMNameByPMCodeView(APIView):
    def get(self, request, PMCode):
        rmcode = PackingMaterials.objects.get(PMCode=PMCode)
        serializer = PMNameSerializer(rmcode)
        return Response(serializer.data)

class PMFormulationsView(generics.CreateAPIView):
    serializer_class = PMFormulationSerializer
    queryset = PMFormulation.objects.all()


class PMDataView(APIView):
    def get(self, request, PMCode):
        pm = PackingMaterials.objects.get(PMCode=PMCode)
        serializer = PMDataSerializer(pm)
        return Response(serializer.data)

class PackSizesView(APIView):
    def get(self, request,PCode):
        size = PackSizes.objects.filter(ProductCode=PCode)
        serializer = PackSizeSerializer(size, many=True)
        return Response(serializer.data)

#-------------------- EDIT PM Formulation ----------------------#

class ProductPMFormulationView(APIView):
    def get(self, request, Pcode):

        formulation = PMFormulation.objects.filter(ProductCode=Pcode)
        dict = []
        for i in formulation:
            dic = {}
            dic['ProductCode'] = i.ProductCode.ProductCode
            dic['Product'] = i.ProductCode.Product
            dic['PackSize'] = i.PackSize.PackSize
            dic['RMCode'] = i.RMCode.RMCode
            dic['Material'] = i.PMCode.Material
            dic['batchSize'] = i.batchSize
            dic['quantity'] = i.quantity
            dict.append(dic)
        return Response(dict)

class FPCodeView(APIView):
    def get(self, request):
        li = PMFormulation.objects.values_list('ProductCode')
        pcode = Products.objects.filter(ProductCode__in=li)
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class FPNameView(APIView):
    def get(self, request):
        li = PMFormulation.objects.values_list('ProductCode')
        pcode = Products.objects.filter(ProductCode__in=li)
        serializer = PNameSerializer(pcode, many=True)
        return Response(serializer.data)
