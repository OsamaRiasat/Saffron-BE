from django.db.models import Max
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from MaterialSuppliers.utils import supplierApprovedItemsCodesList
from .utils import demandedItemsCodesList


# Raw Materials

class RawMaterialTypesViews(viewsets.ModelViewSet):
    serializer_class = RawMaterialTypesSerializer
    queryset = RawMaterialTypes.objects.all()


class RawMaterialsViews(viewsets.ModelViewSet):
    serializer_class = RawMaterialsSerializer
    queryset = RawMaterials.objects.all()


class RawMaterialCodesViews(viewsets.ModelViewSet):
    serializer_class = RawMaterialCodesSerializer
    queryset = RawMaterials.objects.all()


class RawMaterialNamesViews(viewsets.ModelViewSet):
    serializer_class = RawMaterialNamesSerializer
    queryset = RawMaterials.objects.all()


class RawMaterialSearchByRMCode(APIView):
    def get(self, request, RMCode, format=None):
        data = RawMaterials.objects.filter(RMCode=RMCode)
        serializer = RawMaterialNameTypeUnitSerializer(data, many=True)
        return Response(serializer.data)


class RawMaterialSearchByName(APIView):
    def get(self, request, Material, format=None):
        data = RawMaterials.objects.filter(Material=Material).first()
        serializer = RawMaterialCodeTypeUnitSerializer(data, many=True)
        return Response(serializer.data)


# Packing Materials

class PackingMaterialTypesViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialTypesSerializer
    queryset = PackingMaterialTypes.objects.all()


class PackingMaterialsViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialsSerializer
    queryset = PackingMaterials.objects.all()


# Raw Material Demands

class RMDemandedItemsView(viewsets.ModelViewSet):
    serializer_class = RMDemandItemsSerializer
    queryset = RMDemandedItems.objects.all()


class RMDemandsView(generics.CreateAPIView):
    serializer_class = RMDemandSerializer
    queryset = RMDemands.objects.all()


class RMDemandHighestDNoView(APIView):
    def get(self, request):
        DNo = RMDemands.objects.all().aggregate(Max('DNo'))
        return Response(DNo)


class RMDemandsDNosWithPendingStatus(APIView):
    def get(self, request):
        data = RMDemands.objects.only('DNo').filter(demandStatus="PENDING")
        serialize = RMDemandsDNosSerializer(data, many=True)
        return Response(serialize.data)


# Raw Material Purchase Orders

class RMPurchaseOrdersItemsView(viewsets.ModelViewSet):
    serializer_class = RMPurchaseOrderItemsSerializer
    queryset = RMPurchaseOrderItems.objects.all()


class RMPurchaseOrdersViews(generics.CreateAPIView):
    serializer_class = RMPurchaseOrdersSerializer
    queryset = RMPurchaseOrders.objects.all()


class RMPurchaseOrderHighestPONoView(APIView):
    def get(self, request):
        PONo = RMPurchaseOrders.objects.all().aggregate(Max('PONo'))
        print(PONo)
        return Response(PONo)


class RMPurchaseOrderListOfMaterialsForFormView(APIView):
    def get(self, request, SID, DNo):
        # print("RMCode",RMCode)
        # print("RMCode", DNo)
        l1 = supplierApprovedItemsCodesList(SID)
        l2 = demandedItemsCodesList(DNo)
        intersection = set.intersection(set(l1), set(l2))
        l = []
        for RMCode in intersection:
            dic = {}
            dic["RMCode"] = RMCode
            l.append(dic)
        return Response(l)


class RMPurchaseOrdersWithOpenStatusView(APIView):
    def get(self):
        data = RMPurchaseOrders.objects.filter(Status="PENDING")
        serialize = RMPurchaseOrderPONosSerializer(data, many=True)
        return Response(serialize.data)


class RMPurchaseOrderItemsCodesForReceivingView(APIView):
    def get(self, request, PONo):
        data = RMPurchaseOrderItems.objects.filter(PONo=PONo)
        serialize = RMPurchaseOrderItemsRMCodesSerializer(data, many=True)
        return Response(serialize.data)


# --------------- RECEIVING ------------------------

class RMPurchaseOrderDetailsView(APIView):
    def get(self, request, PONo, RMCode):
        data = RMPurchaseOrderItems.objects.get(PONo=PONo, RMCode=RMCode)
        dic = {}
        dic["Material"] = data.RMCode.Material
        dic["demandedQuantity"] = data.Quantity
        dic["balance"] = data.Pending
        dic["demandedQuantity"] = data.Quantity
        dic["units"] = data.RMCode.Units
        dic["supplierName"] = data.SID.S_Name
        dic["suppplierID"] = data.SID.S_ID

        return Response(dic)


class RMIGPView(generics.CreateAPIView):
    serializer_class = RMIGP
    queryset = RMReceiving.objects.all()


class RMReceivingDetailsView(APIView):
    def get(self,IGPNo):
        data = RMReceiving.objects.get(pk=IGPNo)
        dic = {}
        dic["Material"] = data.RMCode.Material
        dic["demandedQuantity"] = data.Quantity
        dic["balance"] = data.Pending
        dic["demandedQuantity"] = data.Quantity
        dic["units"] = data.RMCode.Units
        dic["supplierName"] = data.SID.S_Name
        dic["suppplierID"] = data.SID.S_ID

        return Response(dic)
