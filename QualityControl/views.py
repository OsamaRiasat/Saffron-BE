from datetime import date
import re
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from .models import *
from Inventory.models import RawMaterials
from .serializers import *


# Create your views here.


# Populate Database


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