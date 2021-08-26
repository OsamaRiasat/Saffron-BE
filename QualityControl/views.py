import re
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from rest_framework.views import APIView
import pandas as pd
from .models import *
from Inventory.models import RawMaterials
from .serializers import *
from Account.models import User
from django_filters.rest_framework import DjangoFilterBackend, filters


# Create your views here.


# Populate Database

class specificationReportingView(generics.ListAPIView):
    queryset = RMSpecificationsItems.objects.all()
    serializer_class = RMSpecificationsItemsForSearchingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['specification','specID__RMCode__Units']

class PopulateParametersView(APIView):
    def get(self, request):
        workbook = pd.read_excel(
            r'C:\Users\usama riasat\Documents\Saffron-Clones\Saffron-Restful-APIs\SaffronProject\QualityControl\parameters.xlsx ',
            sheet_name='Sheet1')
        workbook = workbook.to_numpy()

        for i in workbook:
            t = str(i[0])
            print(t)
            paramater1 = RMParameters.objects.create(parameter=i[0])
            paramater1.save()

        return Response({"Populate": "Done"})

# --------------------- SPECIFICATIONS ------------------------

# A. Raw Materials

# View Specs

class RMCodeListOfSpecificationsView(generics.ListAPIView):
    queryset = RMSpecifications.objects.only('RMCode').filter(QAStatus="ALLOWED")
    serializer_class = AcquireRMCodeListSerializer

class RMMaterialListOfSpecificationsView(APIView):
    def get(self, request):
        rm = RMSpecifications.objects.only('RMCode').filter(QAStatus="ALLOWED")
        li = []
        for i in rm:
            dic = {}
            dic['Material'] = i.RMCode.Material
            li.append(dic)
        return Response(li)

class RMViewSpecificationsView(APIView):
    def get(self, request, RMCode):
        data = {}
        spec = RMSpecifications.objects.get(RMCode=RMCode)
        str1 = spec.SOPNo+" Version:"+str(spec.version)+ " Date:"+ str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = RMSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        return Response(data)

# New Specs

class RMCodeView(APIView):
    def get(self, request):
        rmcode = RawMaterials.objects.all()
        serializer = RMCodeSerializer(rmcode, many=True)
        return Response(serializer.data)

class RMCodeByNameView(APIView):
    def get(self, request, name):

        rmcode = RawMaterials.objects.get(Material=name)
        check = RMSpecifications.objects.filter(RMCode=rmcode.RMCode)
        if check:
            return Response({'message': 'Material have already specifications'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = RMCodeSerializer(rmcode)
            return Response(serializer.data)


class RMaterialView(APIView):
    def get(self, request):
        rm = RawMaterials.objects.all()
        serializer = RMaterialSerializer(rm, many=True)
        return Response(serializer.data)


class RMNameByRMCodeView(APIView):
    def get(self, request, RMCode):
        check = RMSpecifications.objects.filter(RMCode=RMCode)
        if check:
            return Response({'message': 'Material have already specifications'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            rmcode = RawMaterials.objects.get(RMCode=RMCode)
            serializer = RMaterialSerializer(rmcode)
            return Response(serializer.data)


class RMReferenceView(APIView):
    def get(self, request):
        ref = RMReferences.objects.all()
        serializer = RMReferencesSerializer(ref, many=True)
        return Response(serializer.data)


class RMParametersView(APIView):
    def get(self, request):
        ref = RMParameters.objects.all()
        serializer = RMParameterSerializer(ref, many=True)
        return Response(serializer.data)


class RMSpecificationsView(generics.CreateAPIView):
    queryset = RMSpecifications.objects.all()
    serializer_class = RMSpecificationsSerializer


class RMAcquireSpecificationsView(APIView):
    def get(self, request, RMCode):
        spec = RMSpecifications.objects.get(RMCode=RMCode)
        spec_items = RMSpecificationsItems.objects.filter(specID=spec)
        serializer = AcquireSpecificationsItemsSerializer(spec_items, many=True)
        return Response(serializer.data)


class AcquireRMCodeListView(generics.ListAPIView):
    queryset = RMSpecifications.objects.all()
    serializer_class = AcquireRMCodeListSerializer


class AcquireRMaterialListView(APIView):
    def get(self, request):
        rm = RMSpecifications.objects.all()
        li = []
        for i in rm:
            dic = {}
            dic['Material'] = i.RMCode.Material
            li.append(dic)
        return Response(li)

#Edit RM Specs

class RMEditSpecsView(APIView):
    def get(self,request,RMCode):
        # rm=RawMaterials.objects.get(RMCode=RMCode)
        specs = RMSpecifications.objects.get(RMCode=RMCode)
        specs_items = RMSpecificationsItems.objects.filter(specID=specs)
        dict = {}
        dict['RMCode'] = specs.RMCode.RMCode
        dict['reference'] = specs.reference.reference
        dict['SOPNo'] = specs.SOPNo
        dict['date'] = specs.date
        dict['version'] = specs.version
        lis = []
        for i in specs_items:
            dic = {}
            dic['parameter'] = i.parameter.parameter
            dic['specification'] = i.specification
            lis.append(dic)
        dict['items']=lis
        return Response(dict)

class TEMPRMSpecificationsView(generics.CreateAPIView):
    queryset = TempRMSpecifications.objects.all()
    serializer_class = TempRMSpecificationsSerializer

#RM Sample Assignment
class RMSamplesView(APIView):
    def get(self,request):
        samples = RMSamples.objects.all()
        dict = []
        for i in samples:
            dic = {}
            dic['QCNo'] = i.QCNo
            rm_receiving = RMReceiving.objects.get(IGPNo=i.IGPNo.IGPNo)
            rm = RawMaterials.objects.get(RMCode=rm_receiving.RMCode)
            dic['Date'] = i.samplingDateTime
            dic['Material'] = rm.Material
            dic['Unit'] = rm.Units
            dic['Quantity'] = rm_receiving.quantityReceived
            dict.append(dic)
        return Response(dict)

class AnalystView(APIView):
    def get(self,request):
        analysts = User.objects.filter(role="QC_Analyst", is_active=True)
        print(analysts)
        serializer = AnalystSerializer(analysts,many=True)
        return Response(serializer.data)

class AssignAnalystView(generics.UpdateAPIView):
   queryset = RMSamples.objects.all()
   serializer_class = AssignAnalystSerializer

# --------------------- Data Entry ------------------------

# RM Data Entry

class RMQCNoView(APIView):
    def get(self,request):
        user=request.user
        if(user.role=='QC_Analyst'):
            qc = RMSamples.objects.filter(analyst=user.id)
            serializer = RMQCNoSerializer(qc, many=True)
            return Response(serializer.data)
        else:
            return Response({'message':'There is no QC sample for this Analyst'})

class RMQCNoSampleView(APIView):
    def get(self,request,QCNo):
        sample=RMSamples.objects.get(QCNo=QCNo)

        rm_receiving=RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
        
        dict={}
        dict['samplingDateTime']=sample.samplingDateTime
        dict['QCNo']=QCNo
        dict['IGPNo']=sample.IGPNo.IGPNo
        dict['assignedDateTime']=sample.assignedDateTime
        dict['analyst']=sample.analyst.username
        
        dict['RMCode']=rm_receiving.RMCode.RMCode
        dict['Material']=rm_receiving.RMCode.Material
        dict['Units']=rm_receiving.RMCode.Units
        dict['quantityReceived']=rm_receiving.quantityReceived
        dict['batchNo']=rm_receiving.batchNo
        dict['MFG_Date']=rm_receiving.MFG_Date
        dict['EXP_Date']=rm_receiving.MFG_Date

        data = {}
        spec = RMSpecifications.objects.get(RMCode=rm_receiving.RMCode.RMCode)
        str1 = spec.SOPNo+" Version:"+str(spec.version)+ " Date:"+ str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = RMSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        dict['result'] = data
        return Response(dict)

class PostRMAnalysisView(generics.CreateAPIView):
    queryset = RMAnalysis.objects.all()
    serializer_class = PostRMAnalysisSerializer

    #----------------------Block Analyst------------------------------#

class BlockUnBlockAnalystView(APIView):
    def get(self,request,id):
        user=User.objects.get(id=id)
        if user.is_active==True:
            user.is_active=False
        else:
            user.is_active=True        
        user.save()
        return Response({'message':'userblocked'})

class AllAnalystView(APIView):
    def get(self,request):
        user=User.objects.filter(role='QC_Analyst')
        dict=[]
        for i in user:
            dic={}
            dic['id']=i.id
            dic['username']=i.username
            if i.is_active==False:
                dic['status']='UnBlock'
            else:
                dic['status']='Block'
            dict.append(dic)
        return Response(dict)
            