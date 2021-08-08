from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Inventory.models import RawMaterials
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
        l = []
        for obj in data:
            dic = {}
            Materials = RawMaterials.objects.filter(pk=obj.MCode).only('Material')
            dic["Material"] = Materials.get().Material
            l.append(dic)
        print(l)

        return Response(l)
