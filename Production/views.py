import re
from QualityControl.views import PostRMCOAApprovalView
from Products.models import Formulation
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from Planning.models import *
from .serializers import *
from datetime import date
from dateutil.relativedelta import relativedelta
from .utils import CreateBatchNo, getStandardBatchSize
# Create your views here.

#------------------Batch Issuence Request--------------------#
class PlanNoView(APIView):
    def get(self,request):
        plans = PlanItems.objects.filter(status='OPEN').values_list('planNo').distinct()
        entries = PlanItems.objects.filter(id__in=plans)
        serializer = PlanNoSerializer(entries, many=True)
        return Response(serializer.data)

class ProductByPlanNoView(APIView): #retrieve only distinct
    def get(self,request,planNo):
        product = PlanItems.objects.filter(planNo=planNo).values_list('ProductCode').distinct()
        dict = []
        for i in product:
            dic = {}
            dic['ProductCode'] = i[0]
            dict.append(dic)
        return Response(dict)

class SBSView(APIView):
    def get(self,request,PCode):
        size = getStandardBatchSize(PCode)
        return Response({'Units':size})

class BatchIssuenceRequestView(generics.CreateAPIView):
    queryset = BatchIssuanceRequest.objects.all()
    serializer_class = BatchIssuenceRequestSerializer


class PlanNoBIRView(APIView):
    def get(self,request):
        plans = BatchIssuanceRequest.objects.filter(noOfBatches__gt=0).values_list('planNo').distinct()
        entries = BatchIssuanceRequest.objects.filter(planNo__in=plans)
        serializer = PlanNoBIRSerializer(entries,many=True)
        return Response(serializer.data)

class PCodeBIRView(APIView):
    def get(self,request,planNo):
        plans = BatchIssuanceRequest.objects.filter(planNo=planNo).values_list('ProductCode').distinct()
        entries = BatchIssuanceRequest.objects.filter(ProductCode__in=plans)
        serializer = PCodeBIRSerializer(entries,many=True)
        return Response(serializer.data)

class IssueBatchNoView(APIView):
    serializer_class=PlanPCodeSerializer
    def post(self,request):
        data = request.data
        planNo = data.get('planNo',None)
        Pcode = data.get('ProductCode',None)
        product = Products.objects.get(ProductCode=Pcode)
        dict = {}
        dict['Date'] = date.today()
        dict['planNo'] = planNo
        dict['Product'] = product.Product
        dict['Dosage'] = product.dosageForm.dosageForm
        dict['batchSize'] = getStandardBatchSize(Pcode)
        dict['MFG_Date'] = date.today()
        shelf_life = Products.objects.get(ProductCode=Pcode).ShelfLife
        dict['EXP_Date'] = (date.today() + relativedelta(years=+shelf_life))
        batchNo = CreateBatchNo(Pcode)
        dict['batchNo'] = batchNo
        return Response(dict)

class FormulationView(APIView):
    serializer_class=PCodeBatchSizeSerializer
    def post(self,request):
        data = request.data
        batch_size = data.get('batchSize',None)
        Pcode = data.get('Pcode',None)
        sbs = getStandardBatchSize(Pcode)
        total = batch_size/sbs
        formulation = Formulation.objects.filter(ProductCode=Pcode)
        dict = []
        for i in formulation:
            dic={}
            dic['Type'] = i.RMCode.Type.Type
            dic['RMCode'] = i.RMCode.RMCode
            dic['Material'] = i.RMCode.Material
            dic['Units'] = i.RMCode.Units
            dic['Quantity'] = float(i.quantity)*float(total)
            dict.append(dic)
        return Response(dict)

class BPRLogView(generics.CreateAPIView):
    queryset = BPRLog.objects.all()
    serializer_class = BPRLogSerializer

#----------- Batch Track --------------#

class PCodeBPRView(APIView):
    def get(self,request):
        pcode = BPRLog.objects.filter(batchStatus='OPEN').values_list('ProductCode').distinct()
        entries = BPRLog.objects.filter(ProductCode__in=pcode)
        serializer = PCodeBPRSerializer(entries,many=True)
        return Response(serializer.data)

class BatchNoBPRView(APIView):
    def get(self,request,PCode):
        batchNo = BPRLog.objects.filter(ProductCode=PCode)
        serializer = BatchNoBPRSerializer(batchNo,many=True)
        return Response(serializer.data)

class GeneralDataBPRLogView(APIView):
    serializer_class = PCodeBatchNoBPRSerializer
    def post(self,request):
        data = request.data
        pcode = data.get('ProductCode',None)
        batchNo = data.get('batchNo',None)
        gdata = BPRLog.objects.get(ProductCode=pcode,batchNo=batchNo)
        dict = {}
        dict['currentStage'] = gdata.currentStage
        dict['ProductCode'] = pcode
        dict['batchNo'] = batchNo
        dict['batchSize'] = gdata.batchSize
        dict['MFGDate'] = gdata.MFGDate
        dict['EXPDate'] = gdata.EXPDate
        li=[]
        stages=BatchStages.objects.filter(batchNo=batchNo)
        for i in stages:
            dic={}
            dic['currentStage'] = i.currentStage
            dic['openingDate'] = i.openingDate
            dic['closingDate'] = i.closingDate
            dic['units'] = i.units
            dic['theoreticalYield'] = i.theoreticalYield
            dic['actualYield'] = i.actualYield
            dic['yieldPercentage'] = i.yieldPercentage
            dic['PartialStatus'] = i.PartialStatus
            li.append(dic)
        dict['batchStages'] = li
        return Response(dict)

class BatchStagesView(generics.CreateAPIView):
    queryset = BatchStages.objects.all()
    serializer_class = BatchStagesSerializer

class DataFromBPRView(APIView):
    def get(self,request,PCode):
        data = BPRLog.objects.filter(ProductCode=PCode, batchStatus='OPEN')
        serializer = DataFromBPRSerializer(data, many=True)
        return Response(serializer.data)

#-------- Paking ---------#

class PackSizeDosageView(APIView):
    def get(self,request,PCode):
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
        return Response(dict)

class BatchNoFromBPRView(APIView):
    def get(self, request, PCode):
        bno = BPRLog.objects.filter(ProductCode=PCode,currentStage='Packing')
        serializer = BatchNoBPRSerializer(bno,many=True)
        return Response(serializer.data)
        
class PackingLogView(generics.CreateAPIView):
    queryset = PackingLog.objects.all()
    serializer_class = PackingLogSerializer