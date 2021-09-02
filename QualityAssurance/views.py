from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from Inventory.models import RMReceiving, PMReceiving
from QualityControl.models import RMSamples, PMSamples
from rest_framework.response import Response
from .utils import *


# Create your views here.


#   ----------------------- RM SAMPLE ----------------------

class GRNOListView(APIView):
    def get(self, request):
        grn = RMReceiving.objects.filter(status='QUARANTINED', GRNo__gt=0)
        serializer = GRNOListSerializer(grn, many=True)
        return Response(serializer.data)


class RMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = RMReceiving.objects.get(GRNo=GRNo)
        dic = {}
        dic["GRNo"] = GRNo
        dic["Material"] = data.RMCode.Material
        dic['RMCode'] = data.RMCode.RMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic['MFG_Date'] = data.MFG_Date
        dic['EXP_Date'] = data.EXP_Date
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = data.RMCode.Units
        dic['containersReceived'] = data.containersReceived

        dic["QC_No"] = getQCNO()

        return Response(dic)


class RMSampleView(generics.CreateAPIView):
    queryset = RMSamples.objects.all()
    serializer_class = RMSampleSerializer


#   ----------------------- PM SAMPLE ----------------------

class PMGRNOListView(APIView):
    def get(self, request):
        grn = PMReceiving.objects.filter(status='QUARANTINED', GRNo__gt=0)
        serializer = GRNOListSerializer(grn, many=True)
        return Response(serializer.data)


class PMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = PMReceiving.objects.get(GRNo=GRNo)
        dic = {}
        dic["GRNo"] = GRNo
        dic["Material"] = data.PMCode.Material
        dic['RMCode'] = data.PMCode.PMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic['MFG_Date'] = data.MFG_Date
        dic['EXP_Date'] = data.EXP_Date
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = data.PMCode.Units
        dic['containersReceived'] = data.containersReceived

        dic["QC_No"] = PMgetQCNO()

        return Response(dic)


class PMSampleView(generics.CreateAPIView):
    queryset = PMSamples.objects.all()
    serializer_class = PMSampleSerializer
