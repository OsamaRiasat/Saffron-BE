from django.db.models import Max
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from Planning.models import Plan, ProductMaterials, ProductPackingMaterials
from Production.models import BPRLog
from Production.serializers import BPRSerializer
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from MaterialSuppliers.utils import supplierApprovedItemsCodesList, supplierApprovedItemsNamesList
from .utils import demandedItemsCodesList, PMdemandedItemsCodesList, demandedItemsNamesList, PMdemandedItemsNamesList
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


class PlanNosListView(generics.ListAPIView):
    queryset = Plan.objects.all()
    serializer_class = planNumbersSerializer


class Demanded_Materials_Through_PlanNo_View(APIView):
    def get(self, request, planNo):
        data = ProductMaterials.objects.filter(planNo=planNo)
        li = []
        for obj in data:
            if obj.demandedQuantity <= 0:
                continue
            dic = {}
            dic["Category"] = obj.RMCode.Type.Type
            dic["RMCode"] = obj.RMCode.RMCode
            dic["Material"] = obj.RMCode.Material
            dic["demandedQuantity"] = obj.demandedQuantity
            dic["Unit"] = obj.RMCode.Units
            li.append(dic)
        return Response(li)


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


class Demanded_Packing_Materials_Through_PlanNo_View(APIView):
    def get(self, request, planNo):
        data = ProductPackingMaterials.objects.filter(planNo=planNo)
        li = []
        for obj in data:
            if obj.demandedQuantity <= 0:
                continue
            dic = {}
            dic["Category"] = obj.PMCode.Type.Type
            dic["RMCode"] = obj.PMCode.PMCode
            dic["Material"] = obj.PMCode.Material
            dic["demandedQuantity"] = obj.demandedQuantity
            dic["Unit"] = obj.PMCode.Units
            li.append(dic)
        return Response(li)


# Raw Material Purchase Orders

class RMDemandedItemsView(APIView):
    def get(self, request, pk):
        data = RMDemandedItems.objects.filter(DNo=pk)
        serializer = DemandedItemsForViewSerializer(data, many=True)
        return Response(serializer.data)


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


class RMPurchaseOrderListOfMaterialCodesForFormView(APIView):
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


class RMPurchaseOrderListOfMaterialsForFormView(APIView):
    def get(self, request, SID, DNo):
        # print("RMCode",RMCode)
        # print("RMCode", DNo)
        l1 = supplierApprovedItemsNamesList(SID)
        l2 = demandedItemsNamesList(DNo)
        intersection = set.intersection(set(l1), set(l2))
        l = []
        for RMName in intersection:
            dic = {}
            dic["RMName"] = RMName
            l.append(dic)
        return Response(l)


class RMPurchaseOrdersWithOpenStatusView(APIView):
    def get(self, request):
        data = RMPurchaseOrders.objects.filter(Status="PENDING")
        serialize = RMPurchaseOrderPONosSerializer(data, many=True)
        return Response(serialize.data)


class RMPurchaseOrderItemsCodesForReceivingView(APIView):
    def get(self, request, PONo):
        data = RMPurchaseOrderItems.objects.filter(PONo=PONo)
        serialize = RMPurchaseOrderItemsRMCodesSerializer(data, many=True)
        return Response(serialize.data)


# Packing Material Purchase Orders

class PMDemandedItemsView(APIView):
    def get(self, request, pk):
        data = PMDemandedItems.objects.filter(DNo=pk)
        serializer = PMDemandedItemsForViewSerializer(data, many=True)
        return Response(serializer.data)


class PMPurchaseOrdersItemsView(viewsets.ModelViewSet):
    serializer_class = PMPurchaseOrderItemsSerializer
    queryset = PMPurchaseOrderItems.objects.all()


class PMPurchaseOrdersViews(generics.CreateAPIView):
    serializer_class = PMPurchaseOrdersSerializer
    queryset = PMPurchaseOrders.objects.all()


# class PMDemandedItemsView(APIView):
#     def get(self,request, pk):
#         data = PMDemandedItems.objects.filter(DNo=pk)
#         serializer = PMDemandItemsSerializer(data, many=True)
#         return Response(serializer.data)

class PMPurchaseOrderHighestPONoView(APIView):
    @extend_schema(description='text for description')
    def get(self, request):
        PONo = PMPurchaseOrders.objects.all().aggregate(Max('PONo'))
        print(PONo)
        return Response(PONo)


class PMPurchaseOrderListOfMaterialCodesForFormView(APIView):
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


class PMPurchaseOrderListOfMaterialsForFormView(APIView):
    def get(self, request, SID, DNo):
        # print("RMCode",RMCode)
        # print("RMCode", DNo)
        l1 = supplierApprovedItemsNamesList(SID)
        l2 = PMdemandedItemsNamesList(DNo)
        intersection = set.intersection(set(l1), set(l2))
        l = []
        for PMName in intersection:
            dic = {}
            dic["PMName"] = PMName
            l.append(dic)
        return Response(l)


class PMPurchaseOrdersWithOpenStatusView(APIView):
    def get(self, request):
        data = PMPurchaseOrders.objects.filter(Status="PENDING")
        serialize = PMPurchaseOrderPONosSerializer(data, many=True)
        return Response(serialize.data)


class PMPurchaseOrderItemsCodesForReceivingView(APIView):
    def get(self, request, PONo):
        data = PMPurchaseOrderItems.objects.filter(PONo=PONo)
        serialize = PMPurchaseOrderItemsPMCodesSerializer(data, many=True)
        return Response(serialize.data)


# --------------- Raw Materials RECEIVING ------------------------

class RMPurchaseOrderDetailsView(APIView):
    def get(self, request, PONo, RMCode):
        data = RMPurchaseOrderItems.objects.get(PONo=PONo, RMCode=RMCode)
        dic = {}
        dic["Material"] = data.RMCode.Material
        dic["demandedQuantity"] = data.Quantity
        dic["balance"] = data.Pending
        # dic["demandedQuantity"] = data.Quantity
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
    queryset = RMReceiving.objects.all()
    serializer_class = IGPNoSerializer


class RMHighestGRNO(APIView):
    def get(self, request):
        GRNo = RMReceiving.objects.all().aggregate(Max('GRNo'))
        print(GRNo)
        return Response(GRNo)


class RMReceivingDetailsView(APIView):
    def get(self, request, IGPNo):
        data = RMReceiving.objects.get(pk=IGPNo)
        material = RawMaterials.objects.get(RMCode=data.RMCode.RMCode)
        # sname=Suppliers.objects.filter(S_ID=data.S_ID)
        dic = {}
        dic["Recieving_Date"] = data.IGPDate
        dic["Code"] = data.RMCode.RMCode
        dic["Material"] = material.Material
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = material.Units
        dic["Containers"] = data.containersReceived
        return Response(dic)


class UpdateRMReceivingDetailsView(generics.UpdateAPIView):
    serializer_class = UpdateRMRecievingSerializer
    queryset = RMReceiving.objects.all()


# POST GRN


class GRNoView(APIView):
    def get(self, request):
        data = RMReceiving.objects.only('GRNo').filter(status="APPROVED")
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class RMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = RMReceiving.objects.get(GRNo=GRNo)
        material = RawMaterials.objects.get(RMCode=data.RMCode.RMCode)

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
        dic["remarks"] = data.remarks
        return Response(dic)


# RM Print GRN


class GRNoForPrintGRNView(APIView):
    def get(self, request):
        data = RMReceiving.objects.only('GRNo').filter(status="QUARANTINED", GRNo__gt=0)
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class RMReceivingDetailsByGRNoForPrintGRNView(APIView):
    def get(self, request, GRNo):
        data = RMReceiving.objects.get(GRNo=GRNo)
        material = RawMaterials.objects.get(RMCode=data.RMCode.RMCode)

        dic = {}
        dic["IGPNo"] = data.IGPNo
        dic["Approval_Date"] = data.approval_Date
        dic["Material"] = material.Material
        dic["Code"] = material.RMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["containersReceived"] = data.containersReceived
        dic["units"] = material.Units
        dic["Recieving_Date"] = data.IGPDate
        dic["MFG"] = data.MFG_Date
        dic["Exp_Date"] = data.EXP_Date
        dic["remarks"] = data.remarks
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
        material = PackingMaterials.objects.get(PMCode=data.PMCode.PMCode)
        # sname=Suppliers.objects.filter(S_ID=data.S_ID)
        dic = {}
        dic["Recieving_Date"] = data.IGPDate
        dic["Code"] = data.PMCode.PMCode
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

# class PMGRNoView(generics.ListAPIView):
#     queryset = PMReceiving.objects.all()
#     serializer_class = PMGRNoSerializer

class PMGRNoView(APIView):
    def get(self, request):
        data = PMReceiving.objects.only('GRNo').filter(status="APPROVED")
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class PMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = PMReceiving.objects.get(GRNo=GRNo)
        material = PackingMaterials.objects.get(PMCode=data.PMCode.PMCode)

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
        dic["remarks"] = data.remarks
        return Response(dic)


# PM Print GRN


class PMGRNoForPrintGRNView(APIView):
    def get(self, request):
        data = PMReceiving.objects.only('GRNo').filter(status="QUARANTINED", GRNo__gt=0)
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class PMReceivingDetailsByGRNoForPrintGRNView(APIView):
    def get(self, request, GRNo):
        data = PMReceiving.objects.get(GRNo=GRNo)
        material = PackingMaterials.objects.get(PMCode=data.PMCode.PMCode)

        dic = {}
        dic["IGPNo"] = data.IGPNo
        dic["Approval_Date"] = data.approval_Date
        dic["Material"] = material.Material
        dic["Code"] = material.PMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["containersReceived"] = data.containersReceived
        dic["units"] = material.Units
        dic["Recieving_Date"] = data.IGPDate
        dic["MFG"] = data.MFG_Date
        dic["Exp_Date"] = data.EXP_Date
        dic["remarks"] = data.remarks
        return Response(dic)


# ---------------------- Bin Cards -------------------------

# Raw Materials

class RMBinCardView(APIView):
    serializer_class = GRNoSerializer

    def post(self, request):
        data = request.data
        grno = data.get('GRNo', None)
        data = RMReceiving.objects.get(GRNo=grno)
        material = RawMaterials.objects.get(RMCode=data.RMCode.RMCode)
        bin = RMBinCards.objects.create(particulars=data.S_ID.S_Name,
                                        batchNo=data.batchNo,
                                        received=data.quantityApproved,
                                        balance=data.quantityApproved,
                                        # balance= RMBinCards.objects.all().aggregate(Max('DateTime')),
                                        QCNo=data.QCNo,
                                        GRBalance=data.quantityApproved,
                                        RMCode=material)
        bin.save()
        serializer = RMBinCardsSerializer(bin)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data)


# Packing Materials

class PMBinCardView(APIView):
    serializer_class = PMGRNoSerializer

    def post(self, request):
        data = request.data
        grno = data.get('GRNo', None)
        data = PMReceiving.objects.get(GRNo=grno)
        material = PackingMaterials.objects.get(PMCode=data.PMCode.PMCode)
        bin = PMBinCards.objects.create(particulars=data.S_ID.S_Name,
                                        batchNo=data.batchNo,
                                        received=data.quantityApproved,
                                        balance=data.quantityApproved,
                                        # balance= RMBinCards.objects.all().aggregate(Max('DateTime')),
                                        QCNo=data.QCNo,
                                        GRBalance=data.quantityApproved,
                                        PMCode=material)
        bin.save()
        serializer = PMBinCardsSerializer(bin)
        # if serializer.is_valid():
        #     serializer.save()
        return Response(serializer.data)


# Populate Database

class PopulateRawMaterialView(APIView):
    def get(self, request):
        workbook = pd.read_excel(r'C:\Users\hp\Desktop\Store\saff-apis\Inventory\rmTable02.xlsb', sheet_name='RMList')
        workbook = workbook.to_numpy()
        print(workbook)
        for i in workbook:
            t = str(i[3])
            type = RawMaterialTypes.objects.get(Type=t)
            rw = RawMaterials.objects.create(
                RMCode=i[0],
                Material=i[1],
                Units=i[2],
                Type=type
            )
            rw.save()
        return Response({"Populate": "Done"})

    # ------------- RM Dispensing   ------------


class PCodeBPRView(APIView):
    def get(self, request):
        # ProductCode
        # pcode = BPRLog.objects.filter(batchStatus='OPEN').values_list('ProductCode').distinct()
        # entries = BPRLog.objects.filter(ProductCode__in=pcode)
        # serializer = PCodeBPRSerializer(entries, many=True)

        l = []
        d = BPRLog.objects.only('ProductCode').filter(batchStatus='OPEN', currentStage='Dispensing').distinct()
        for i in d:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        l2 = []
        for i in l:
            dic = {}
            dic["ProductCode"] = i
            l2.append(dic)

        return Response(l2)


class BPRByPcodeView(APIView):
    def get(self, request, PCode):
        batchNo = BPRLog.objects.filter(ProductCode=PCode, currentStage="Dispensing")
        serializer = BPRSerializer(batchNo, many=True)
        return Response(serializer.data)


#
# class GeneralDataBPRLogView(APIView):
#     serializer_class = PCodeBatchNoBPRSerializer
#
#     def post(self, request):
#         data = request.data
#         pcode = data.get('ProductCode', None)
#         batchNo = data.get('batchNo', None)
#         gdata = BPRLog.objects.get(ProductCode=pcode, batchNo=batchNo)
#         dict = {}
#         dict['currentStage'] = gdata.currentStage
#         dict['ProductCode'] = pcode
#         dict['batchNo'] = batchNo
#         dict['batchSize'] = gdata.batchSize
#         dict['MFGDate'] = gdata.MFGDate
#         dict['EXPDate'] = gdata.EXPDate
#         li = []
#         stages = BatchStages.objects.filter(batchNo=batchNo)
#         for i in stages:
#             dic = {}
#             dic['currentStage'] = i.currentStage
#             dic['openingDate'] = i.openingDate
#             dic['closingDate'] = i.closingDate
#             dic['units'] = i.units
#             dic['theoreticalYield'] = i.theoreticalYield
#             dic['actualYield'] = i.actualYield
#             dic['yieldPercentage'] = i.yieldPercentage
#             dic['PartialStatus'] = i.PartialStatus
#             li.append(dic)
#         dict['ListToBeAddedInTable'] = li
#
#         data = Stages.objects.filter(dosageForm=gdata.ProductCode.dosageForm)
#         l = []
#         for i in data:
#             l.append(i.stage)
#         dict['ListOfStages'] = l
#
#         return Response(dict)
#

# class BatchStagesView(generics.CreateAPIView):
#     queryset = BatchStages.objects.all()
#     serializer_class = BatchStagesSerializer


# class DataFromBPRView(APIView):
#     def get(self, request, PCode):
#         data = BPRLog.objects.filter(ProductCode=PCode, batchStatus='OPEN')
#         serializer = DataFromBPRSerializer(data, many=True)
#         return Response(serializer.data)


#   ------------  RM  Material Return Note   -------------


class GRNoFor_RM_Return_Note_View(APIView):
    def get(self, request):
        data = RMReceiving.objects.only('GRNo').filter(status="REJECTED")
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class RM_Returned_View(APIView):
    def get(self, request, GRN_No):
        obj = RMReceiving.objects.filter(GRNo=GRN_No).first()
        obj.status = "RETURNED"
        obj.save()
        return Response({"message": "Material Returned."})


#   ------------  PM  Material Return Note   -------------


class GRNoFor_PM_Return_Note_View(APIView):
    def get(self, request):
        data = PMReceiving.objects.only('GRNo').filter(status="REJECTED")
        l = []
        for obj in data:
            dic = {}
            dic["GRNo"] = obj.GRNo
            l.append(dic)
        return Response(l)


class PM_Returned_View(APIView):
    def get(self, request, GRN_No):
        obj = PMReceiving.objects.filter(GRNo=GRN_No).first()
        obj.status = "RETURNED"
        obj.save()
        return Response({"message": "Material Returned."})


#   ------------  RM  Material Return Note   -------------

class RM_Destructed_View(APIView):
    def get(self, request, GRN_No):
        obj = RMReceiving.objects.filter(GRNo=GRN_No).first()
        obj.status = "DESTRUCTED"
        obj.save()
        return Response({"message": "Material Returned."})


#   ------------  PM  Destruction Note   -------------

class PM_Returned_View(APIView):
    def get(self, request, GRN_No):
        obj = PMReceiving.objects.filter(GRNo=GRN_No).first()
        obj.status = "DESTRUCTED"
        obj.save()
        return Response({"message": "Material Returned."})
