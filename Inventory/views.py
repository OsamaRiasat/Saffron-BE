from django.db.models import Max
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from MaterialSuppliers.utils import supplierApprovedItemsCodesList
from .utils import demandedItemsCodesList, PMdemandedItemsCodesList
import pandas as pd

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
        serializer = RawMaterialCodeTypeUnitSerializer(data)
        return Response(serializer.data)


# Packing Materials


class PackingMaterialTypesViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialTypesSerializer
    queryset = PackingMaterialTypes.objects.all()


class PackingMaterialsViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialsSerializer
    queryset = PackingMaterials.objects.all()



class PackingMaterialCodesViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialCodesSerializer
    queryset = PackingMaterials.objects.all()


class PackingMaterialNamesViews(viewsets.ModelViewSet):
    serializer_class = PackingMaterialNamesSerializer
    queryset = PackingMaterials.objects.all()


class PackingMaterialSearchByPMCode(APIView):
    def get(self, request, PMCode, format=None):
        data = PackingMaterials.objects.filter(PMCode=PMCode)
        serializer = PackingMaterialNameTypeUnitSerializer(data, many=True)
        return Response(serializer.data)


class PackingMaterialSearchByName(APIView):
    def get(self, request, Material, format=None):
        data = PackingMaterials.objects.filter(Material=Material).first()
        serializer = PackingMaterialCodeTypeUnitSerializer(data)
        return Response(serializer.data)

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


# Packing Material Demands

class PMDemandedItemsView(viewsets.ModelViewSet):
    serializer_class = PMDemandItemsSerializer
    queryset = PMDemandedItems.objects.all()


class PMDemandsView(generics.CreateAPIView):
    serializer_class = PMDemandSerializer
    queryset = PMDemands.objects.all()


class PMDemandHighestDNoView(APIView):
    def get(self, request):
        DNo = PMDemands.objects.all().aggregate(Max('DNo'))
        return Response(DNo)


class PMDemandsDNosWithPendingStatus(APIView):
    def get(self, request):
        data = PMDemands.objects.only('DNo').filter(demandStatus="PENDING")
        serialize = PMDemandsDNosSerializer(data, many=True)
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
    def get(self,request):
        data = RMPurchaseOrders.objects.filter(Status="PENDING")
        serialize = RMPurchaseOrderPONosSerializer(data, many=True)
        return Response(serialize.data)


class RMPurchaseOrderItemsCodesForReceivingView(APIView):
    def get(self, request, PONo):
        data = RMPurchaseOrderItems.objects.filter(PONo=PONo)
        serialize = RMPurchaseOrderItemsRMCodesSerializer(data, many=True)
        return Response(serialize.data)




# Packing Material Purchase Orders

class PMPurchaseOrdersItemsView(viewsets.ModelViewSet):
    serializer_class = PMPurchaseOrderItemsSerializer
    queryset = PMPurchaseOrderItems.objects.all()


class PMPurchaseOrdersViews(generics.CreateAPIView):
    serializer_class = PMPurchaseOrdersSerializer
    queryset = PMPurchaseOrders.objects.all()


class PMPurchaseOrderHighestPONoView(APIView):
    def get(self, request):
        PONo = PMPurchaseOrders.objects.all().aggregate(Max('PONo'))
        print(PONo)
        return Response(PONo)


class PMPurchaseOrderListOfMaterialsForFormView(APIView):
    def get(self, request, SID, DNo):
        # print("RMCode",RMCode)
        # print("RMCode", DNo)
        l1 = supplierApprovedItemsCodesList(SID)
        l2 = PMdemandedItemsCodesList(DNo)
        intersection = set.intersection(set(l1), set(l2))
        l = []
        for PMCode in intersection:
            dic = {}
            dic["PMCode"] = PMCode
            l.append(dic)
        return Response(l)


class PMPurchaseOrdersWithOpenStatusView(APIView):
    def get(self,request):
        data = PMPurchaseOrders.objects.filter(Status="PENDING")
        serialize = PMPurchaseOrderPONosSerializer(data, many=True)
        return Response(serialize.data)


class PMPurchaseOrderItemsCodesForReceivingView(APIView):
    def get(self, request, PONo):
        data = PMPurchaseOrderItems.objects.filter(PONo=PONo)
        serialize = PMPurchaseOrderItemsRMCodesSerializer(data, many=True)
        return Response(serialize.data)



# --------------- Raw Materials RECEIVING ------------------------

class RMPurchaseOrderDetailsView(APIView):
    def get(self, request, PONo, RMCode):
        data = RMPurchaseOrderItems.objects.get(PONo=PONo, RMCode=RMCode)
        dic = {}
        dic["Material"] = data.RMCode.Material
        dic["demandedQuantity"] = data.Quantity
        dic["balance"] = data.Pending
        #dic["demandedQuantity"] = data.Quantity
        dic["units"] = data.RMCode.Units
        dic["supplierName"] = data.SID.S_Name
        dic["suppplierID"] = data.SID.S_ID

        return Response(dic)

class RMHighestIGPNO(APIView):
    def get(self, request):
        IGPNo = RMReceiving.objects.all().aggregate(Max('IGPNo'))
        print(IGPNo)
        return Response(IGPNo)

class RMIGPView(generics.CreateAPIView):
    serializer_class = RMIGPSerializer
    queryset = RMReceiving.objects.all()


# Generate GRN

class IGPNoView(generics.ListAPIView):
    queryset=RMReceiving.objects.all()
    serializer_class=IGPNoSerializer
class RMHighestGRNO(APIView):
    def get(self, request):
        GRNo = RMReceiving.objects.all().aggregate(Max('GRNo'))
        print(GRNo)
        return Response(GRNo)

class RMReceivingDetailsView(APIView):
    def get(self,request,IGPNo):
        data = RMReceiving.objects.get(pk=IGPNo)
        material=RawMaterials.objects.get(RMCode=data.RMCode)
        #sname=Suppliers.objects.filter(S_ID=data.S_ID)
        dic = {}
        dic["Recieving_Date"]=data.IGPDate
        dic["Code"] = data.RMCode
        dic["Material"] = material.Material
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"]=data.batchNo
        dic["Recieved_Quantity"]=data.quantityReceived
        dic["units"] = material.Units
        dic["Containers"]=data.containersReceived
        return Response(dic)

class UpdateRMReceivingDetailsView(generics.UpdateAPIView):
    serializer_class=UpdateRMRecievingSerializer
    queryset=RMReceiving.objects.all()

# POST GRN

class GRNoView(generics.ListAPIView):
    queryset=RMReceiving.objects.all()
    serializer_class=GRNoSerializer

class RMReceivingDetailsByGRNoView(APIView):
    def get(self,request,GRNo):
        data = RMReceiving.objects.get(pk=GRNo)
        material=RawMaterials.objects.get(RMCode=data.RMCode)
        
        dic = {}
        dic["Approval_Date"]=data.approval_Date
        dic["Material"] = material.Material
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"]=data.batchNo
        dic["Recieved_Quantity"]=data.quantityReceived
        dic["units"] = material.Units
        dic["Approved_Quantity"]=data.quantityApproved
        dic["QC_No"]=data.QCNo
        dic["MFG"]=data.MFG_Date
        dic["Exp_Date"]=data.EXP_Date
        return Response(dic)


# --------------- Packing Materials RECEIVING ------------------------

class PMPurchaseOrderDetailsView(APIView):
    def get(self, request, PONo, PMCode):
        data = PMPurchaseOrderItems.objects.get(PONo=PONo, PMCode=PMCode)
        dic = {}
        dic["Material"] = data.PMCode.Material
        dic["demandedQuantity"] = data.Quantity
        dic["balance"] = data.Pending
        # dic["demandedQuantity"] = data.Quantity
        dic["units"] = data.PMCode.Units
        dic["supplierName"] = data.SID.S_Name
        dic["suppplierID"] = data.SID.S_ID

        return Response(dic)


class PMHighestIGPNO(APIView):
    def get(self, request):
        IGPNo = PMReceiving.objects.all().aggregate(Max('IGPNo'))
        print(IGPNo)
        return Response(IGPNo)


class PMIGPView(generics.CreateAPIView):
    serializer_class = PMIGPSerializer
    queryset = PMReceiving.objects.all()


# Generate GRN

class PMIGPNoView(generics.ListAPIView):
    queryset = PMReceiving.objects.all()
    serializer_class = PMIGPNoSerializer


class PMHighestGRNO(APIView):
    def get(self, request):
        GRNo = PMReceiving.objects.all().aggregate(Max('GRNo'))
        print(GRNo)
        return Response(GRNo)


class PMReceivingDetailsView(APIView):
    def get(self, request, IGPNo):
        data = PMReceiving.objects.get(pk=IGPNo)
        material = PackingMaterials.objects.get(PMCode=data.PMCode)
        # sname=Suppliers.objects.filter(S_ID=data.S_ID)
        dic = {}
        dic["Recieving_Date"] = data.IGPDate
        dic["Code"] = data.PMCode
        dic["Material"] = material.Material
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = material.Units
        dic["Containers"] = data.containersReceived
        return Response(dic)


class UpdatePMReceivingDetailsView(generics.UpdateAPIView):
    serializer_class = UpdatePMRecievingSerializer
    queryset = PMReceiving.objects.all()


# POST GRN

class PMGRNoView(generics.ListAPIView):
    queryset = PMReceiving.objects.all()
    serializer_class = PMGRNoSerializer


class PMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = PMReceiving.objects.get(pk=GRNo)
        material = PackingMaterials.objects.get(PMCode=data.PMCode)

        dic = {}
        dic["Approval_Date"] = data.approval_Date
        dic["Material"] = material.Material
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = material.Units
        dic["Approved_Quantity"] = data.quantityApproved
        dic["QC_No"] = data.QCNo
        dic["MFG"] = data.MFG_Date
        dic["Exp_Date"] = data.EXP_Date
        return Response(dic)

 # ---------------------- Bin Cards -------------------------

 # Raw Materials

class RMBinCardView(APIView):
    serializer_class=GRNoSerializer
    def post(self,request):
        data=request.data
        grno=data.get('GRNo',None)
        data = RMReceiving.objects.get(pk=grno)
        material=RawMaterials.objects.get(RMCode=data.RMCode)
        bin=RMBinCards.objects.create(particulars=data.S_ID.S_Name,
                                    batchNo=data.batchNo,
                                    received=data.quantityApproved,
                                    balance=data.quantityApproved,
                                    #balance= RMBinCards.objects.all().aggregate(Max('DateTime')),
                                    QCNo=data.QCNo,
                                    GRBalance=data.quantityApproved,
                                    RMCode=material)
        bin.save()
        serializer=RMBinCardsSerializer(bin)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data)



 # Packing Materials

class PMBinCardView(APIView):
    serializer_class=PMGRNoSerializer
    def post(self,request):
        data=request.data
        grno=data.get('GRNo',None)
        data = PMReceiving.objects.get(pk=grno)
        material=PackingMaterials.objects.get(PMCode=data.PMCode)
        bin=PMBinCards.objects.create(particulars=data.S_ID.S_Name,
                                    batchNo=data.batchNo,
                                    received=data.quantityApproved,
                                    balance=data.quantityApproved,
                                    #balance= RMBinCards.objects.all().aggregate(Max('DateTime')),
                                    QCNo=data.QCNo,
                                    GRBalance=data.quantityApproved,
                                    PMCode=material)
        bin.save()
        serializer=PMBinCardsSerializer(bin)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data)


#Populate Database

class PopulateRawMaterialView(APIView):
    def get(self,request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Inventory\rmTable02.xlsb',sheet_name='RMList')
        workbook=workbook.to_numpy()
        print(workbook)
        for i in workbook:
            t=str(i[3])
            type=RawMaterialTypes.objects.get(Type=t)
            rw=RawMaterials.objects.create(
                RMCode=i[0],
                Material=i[1],
                Units=i[2],
                Type=type
            )
            rw.save()
        return Response({"Populate":"Done"})