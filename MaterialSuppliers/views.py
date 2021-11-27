from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Inventory.models import RawMaterials,PackingMaterials
from Inventory.serializers import RawMaterialNamesSerializer


# Suppliers

class SuppliersViews(viewsets.ModelViewSet):
    serializer_class = SuppliersSerializer
    queryset = Suppliers.objects.all()


class SupplierIDsViews(viewsets.ModelViewSet):
    serializer_class = SupplierIDSsSerializer
    queryset = Suppliers.objects.all()


class SupplierApprovedItemsViews(viewsets.ModelViewSet):
    serializer_class = SupplierApprovedItemsSerializer
    queryset = SupplierApprovedItems.objects.all()


class SupplierApprovedMaterialsView(APIView):
    def get(self, request, pk, format=None):
        data = SupplierApprovedItems.objects.filter(S_ID=pk)  # This will give objects of approved items having this SID
        obj2 = Suppliers.objects.get(S_ID=pk)
        l = []
        for obj in data:
            dic = {}
            if obj.materialType=="RM":
                Materials = RawMaterials.objects.filter(pk=obj.MCode).only('Material')
                dic["Material"] = Materials.get().Material
                l.append(dic)
            else:
                Materials = PackingMaterials.objects.filter(pk=obj.MCode).only('Material')
                dic["Material"] = Materials.get().Material
                l.append(dic)

        return Response(l)

class suppliers(generics.ListAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer

