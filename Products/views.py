from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import *
from QualityControl.serializers import RMCodeSerializer, RMaterialSerializer
import pandas as pd


class FormulationsView(generics.CreateAPIView):
    serializer_class = FormulationSerializer
    queryset = Formulation.objects.all()


# Populate DB
class PopulateProductView(APIView):
    def get(self, request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Products\prodTable01.xlsx',
                                 sheet_name='ProductList')
        workbook = workbook.to_numpy()
        for i in workbook:
            dform = str(i[3])
            dform = DosageForms.objects.get(dosageForm=dform)
            rw = Products.objects.create(
                ProductCode=i[1],
                Product=i[2],
                RegistrationNo=i[0],
                RegistrationDate=i[7],
                RenewalDate=i[8],
                GenericName=i[4],
                Composition=i[5],
                ShelfLife=i[6],
                dosageForm=dform
            )
            rw.save()
        return Response({"Populate": "Done"})


class PopulateRMFormulationView(APIView):
    def get(self, request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Products\RMFormulation.xlsx')
        workbook = workbook.to_numpy()
        print(workbook)
        for i in workbook:
            p = str(i[0])
            m = str(i[3])
            dno = str(i[9])
            product = Products.objects.get(Product=p)
            material = RawMaterials.objects.get(RMCode=m)
            rw = Formulation.objects.create(
                ProductCode=product,
                RMCode=material,
                batchSize=i[1],
                quantity=i[6],
                date=i[8],
                docNo=dno
            )
            rw.save()
        return Response({"Populate": "Done"})


# ----------------------New Formulation ----------------------#

class PCodeView(APIView):
    def get(self, request):
        li = Formulation.objects.values_list('ProductCode')
        pcode = Products.objects.exclude(ProductCode__in=li)
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class PNameView(APIView):
    def get(self, request):
        li = Formulation.objects.values_list('ProductCode')
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


class RMCodeView(APIView):
    def get(self, request):
        rmcode = RawMaterials.objects.all()
        serializer = RMCodeSerializer(rmcode, many=True)
        return Response(serializer.data)


class RMNameView(APIView):
    def get(self, request):
        rmcode = RawMaterials.objects.all()
        serializer = RMaterialSerializer(rmcode, many=True)
        return Response(serializer.data)


class RMCodeByNameView(APIView):
    def get(self, request, RMName):
        rmcode = RawMaterials.objects.get(Material=RMName)
        serializer = RMCodeSerializer(rmcode)
        return Response(serializer.data)


class RMNameByRMCodeView(APIView):
    def get(self, request, RMCode):
        rmcode = RawMaterials.objects.get(RMCode=RMCode)
        serializer = RMaterialSerializer(rmcode)
        return Response(serializer.data)


class RMDataView(APIView):
    def get(self, request, RMCode):
        rm = RawMaterials.objects.get(RMCode=RMCode)
        serializer = RMDataSerializer(rm)
        return Response(serializer.data)


# ---------------- Edit Formulation -----------------------#

class FPCodeView(APIView):
    def get(self, request):
        li = Formulation.objects.values_list('ProductCode')
        pcode = Products.objects.filter(ProductCode__in=li)
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class FPNameView(APIView):
    def get(self, request):
        li = Formulation.objects.values_list('ProductCode')
        pcode = Products.objects.filter(ProductCode__in=li)
        serializer = PNameSerializer(pcode, many=True)
        return Response(serializer.data)


class ProductFormulationView(APIView):
    def get(self, request, Pcode):
        formulation = Formulation.objects.filter(ProductCode=Pcode)
        dict = []
        for i in formulation:
            dic = {}
            dic['ProductCode'] = i.ProductCode.ProductCode
            dic['Product'] = i.ProductCode.Product
            dic['RMCode'] = i.RMCode.RMCode
            dic['Material'] = i.RMCode.Material
            dic['batchSize'] = i.batchSize
            dic['quantity'] = i.quantity
            dict.append(dic)
        return Response(dict)
