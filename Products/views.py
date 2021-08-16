from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response

import pandas as pd

class FormulationsView(generics.CreateAPIView):
    serializer_class = FormulationSerializer
    queryset = Formulation.objects.all()

#Populate DB
class PopulateProductView(APIView):
    def get(self,request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Products\prodTable01.xlsx',sheet_name='ProductList')
        workbook=workbook.to_numpy()
        for i in workbook:
            dform=str(i[3])
            dform=DosageForms.objects.get(dosageForm=dform)
            rw=Products.objects.create(
                ProductCode = i[1],
                Product = i[2],
                RegistrationNo = i[0],
                RegistrationDate = i[7],
                RenewalDate = i[8],
                GenericName = i[4],
                Composition = i[5],
                ShelfLife = i[6],
                dosageForm = dform
            )
            rw.save()
        return Response({"Populate":"Done"})

class PopulateRMFormulationView(APIView):
    def get(self,request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Products\RMFormulation.xlsx')
        workbook=workbook.to_numpy()
        print(workbook)
        for i in workbook:
            p=str(i[0])
            m=str(i[3])
            dno=str(i[9])
            product=Products.objects.get(Product=p)
            material=RawMaterials.objects.get(RMCode=m)
            rw=Formulation.objects.create(
                ProductCode = product,
                RMCode = material,
                batchSize = i[1],
                quantity = i[6],
                date = i[8],
                docNo = dno
                
            )
            rw.save()
        return Response({"Populate":"Done"})