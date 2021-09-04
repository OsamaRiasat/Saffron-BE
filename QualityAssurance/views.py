from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView

from Production.serializers import BPRSerializer
from .models import *
from .serializers import *
from Inventory.models import RMReceiving, PMReceiving
from QualityControl.models import RMSamples, PMSamples
from rest_framework.response import Response
from .utils import *
import pandas as pd
from Account.models import User
from datetime import date


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


# Populate category model

class PopulateCategoryView(APIView):
    def get(self, request):
        workbook = pd.read_excel(r'C:\Users\usama riasat\Documents\s-clone\saff-apis\QualityAssurance\FormsQA.xlsx',
                                 sheet_name='Category')
        workbook = workbook.to_numpy()
        for i in workbook:
            cat = NCCategory.objects.create(
                category=i[0],
                subCategory=i[1]
            )
            cat.save()
        return Response({"Populate": "Done"})


# -------------------- NCR ------------------------

class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = AllUsersSerializer(users, many=True)
        return Response(serializer.data)


class CategoriesView(APIView):
    def get(self, request):
        cat = NCCategory.objects.values_list('category').distinct()
        li = []
        for i in cat:
            dic = {}
            dic['category'] = i[0]
            li.append(dic)
        return Response(li)


class SubCategoriesView(APIView):
    def get(self, request, category):
        cat = NCCategory.objects.filter(category=category)
        serializer = SubCategoriesSerializer(cat, many=True)
        return Response(serializer.data)


class BatchNoView(APIView):
    def get(self, request, Pcode):
        bno = BPRLog.objects.filter(ProductCode=Pcode, batchStatus='OPEN')
        serializer = BatchNoSerializer(bno, many=True)
        return Response(serializer.data)


class HighestNCRView(APIView):
    def get(self, request):
        ncr1 = 0

        ncr1 = NCR.objects.aggregate(Max('NCRNo'))
        ncr1 = ncr1['NCRNo__max']
        if ncr1 is None:
            ncr1 = 0
        dic = {'NCRNo': ncr1}
        return Response(dic)


class NCRView(generics.CreateAPIView):
    queryset = NCR.objects.all()
    serializer_class = NCRSerializer


class NCRNoView(APIView):
    def get(self, request):
        ncrno = NCR.objects.all()
        serializer = NCRNoSerializer(ncrno, many=True)
        return Response(serializer.data)


class NCRDetailView(APIView):
    def get(self, request, NCRNo):
        nc = NCR.objects.get(NCRNo=NCRNo)
        dict = {}
        dict['date'] = nc.date
        dict['NCRNo'] = nc.NCRNo
        dict['status '] = nc.status
        dict['originator'] = nc.originator
        dict['section'] = nc.section
        dict['sourceOfIdentification'] = nc.sourceOfIdentification
        dict['refNo'] = nc.refNo
        dict['natureOfNC'] = nc.natureOfNC
        dict['gradeOfNC'] = nc.gradeOfNC
        dict['category'] = nc.category
        dict['subCategory'] = nc.subCategory
        dict['batchNo'] = nc.batchNo.batchNo
        dict['Product'] = nc.batchNo.ProductCode.Product
        dict['descriptionOFNonConformance'] = nc.descriptionOFNonConformance
        dict['solutionOfCurrentProblem'] = nc.solutionOfCurrentProblem
        dict['immediateAction'] = nc.immediateAction
        dict['isActionTaken'] = nc.isActionTaken
        dict['actionDate'] = nc.actionDate
        dict['verifiedBy'] = nc.verifiedBy
        dict['isLimitAction'] = nc.isLimitAction
        dict['rootCause'] = nc.rootCause
        dict['proposedCorrectiveAction'] = nc.proposedCorrectiveAction
        dict['actionTaken'] = nc.actionTaken
        return Response(dict)


# ------------------- NCR Close ---------------------#

class NCRNoStatusOpenView(APIView):
    def get(self, request):
        ncrno = NCR.objects.filter(status='OPEN')
        serializer = NCRNoSerializer(ncrno, many=True)
        return Response(serializer.data)


class CloseNCRView(generics.UpdateAPIView):
    queryset = NCR.objects.all()
    serializer_class = CloseNCRSerializer


# ------------------- Batch Close ---------------------#

class OpenBatchesView(APIView):
    def get(self, request):
        data = BPRLog.objects.filter(batchStatus='OPEN')
        serializer = BPRSerializer(data, many=True)
        return Response(serializer.data)


class CloseBPRView(generics.UpdateAPIView):
    queryset = BPRLog.objects.all()
    serializer_class = CloseBPRSerializer