from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Inventory.models import RawMaterials, PackingMaterials
from Inventory.serializers import RawMaterialNamesSerializer


# Add Suppliers

class AddSupplierView(generics.CreateAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersAllFieldsSerializer


# Approve Material For A Supplier
class ShowSuppliersView(generics.ListAPIView):
    serializer_class = SuppliersAllFieldsSerializer
    queryset = Suppliers.objects.all()


class RawMaterialsNamesAndCodeView(generics.ListAPIView):
    serializer_class = RawMaterialSerializer
    queryset = RawMaterials.objects.all()


# class PackingMaterialsNamesAndCodeView(generics.ListAPIView):
#     serializer_class = PackingMaterialSerializer
#     queryset = PackingMaterials.objects.all()

# {
#     "PMCode": "3.01.002.00005",
#     "Material": "Printed Aluminium Foil Winpram (PS)"
#   },
class PackingMaterialsNamesAndCodeView(APIView):
    def get(self, request):
        data = PackingMaterials.objects.all()
        li = []
        for d in data:
            print(d)
            dic = {}
            dic["RMCode"] = d.PMCode
            dic["Material"] = d.Material
            li.append(dic)
        return Response(li)

class AddMaterialToSuppliersView(APIView):
    serializer_class = SupplierApprovedItemsSerializer

    def post(self, request, format=None):
        data = request.data
        MCode = data.get('MCode')
        type = data.get('materialType')
        S_ID = data.get('S_ID')
        obj = SupplierApprovedItems.objects.create(MCode=MCode,
                                                   type=type,
                                                   S_ID=S_ID)
        obj.save()
        return Response({'message': "Material Added"}, status=status.HTTP_200_OK)


class SupplierApprovedMaterialsView(APIView):
    def get(self, request, pk, format=None):
        data = SupplierApprovedItems.objects.filter(S_ID=pk)  # This will give objects of approved items having this SID
        obj2 = Suppliers.objects.get(S_ID=pk)
        l = []
        for obj in data:
            dic = {}
            if obj.materialType == "RM":
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
