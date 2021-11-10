from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from django.shortcuts import render
from rest_framework.views import APIView

from Production.models import Stages
from Production.serializers import BPRSerializer
from Products.models import DosageForms, PackSizes
from .models import *
from .serializers import *
from Inventory.models import RMReceiving, PMReceiving
from QualityControl.models import RMSamples, PMSamples
from rest_framework.response import Response
from .utils import *
import pandas as pd
from Account.models import User
from datetime import date


# Create your views here.


#   ----------------------- RM SAMPLE ----------------------

class GRNOListView(APIView):
    def get(self, request):
        grn = RMReceiving.objects.filter(status='QUARANTINED', GRNo__gt=0)
        serializer = GRNOListSerializer(grn, many=True)
        return Response(serializer.data)


class RMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = RMReceiving.objects.get(GRNo=GRNo)
        dic = {}
        dic["GRNo"] = GRNo
        dic["Material"] = data.RMCode.Material
        dic['RMCode'] = data.RMCode.RMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic['MFG_Date'] = data.MFG_Date
        dic['EXP_Date'] = data.EXP_Date
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = data.RMCode.Units
        dic['containersReceived'] = data.containersReceived

        dic["QC_No"] = getQCNO()

        return Response(dic)


class RMSampleView(generics.CreateAPIView):
    queryset = RMSamples.objects.all()
    serializer_class = RMSampleSerializer


#   ----------------------- PM SAMPLE ----------------------

class PMGRNOListView(APIView):
    def get(self, request):
        grn = PMReceiving.objects.filter(status='QUARANTINED', GRNo__gt=0)
        serializer = GRNOListSerializer(grn, many=True)
        return Response(serializer.data)


class PMReceivingDetailsByGRNoView(APIView):
    def get(self, request, GRNo):
        data = PMReceiving.objects.get(GRNo=GRNo)
        dic = {}
        dic["GRNo"] = GRNo
        dic["Material"] = data.PMCode.Material
        dic['RMCode'] = data.PMCode.PMCode
        dic["supplierName"] = data.S_ID.S_Name
        dic['MFG_Date'] = data.MFG_Date
        dic['EXP_Date'] = data.EXP_Date
        dic["Batch_No"] = data.batchNo
        dic["Recieved_Quantity"] = data.quantityReceived
        dic["units"] = data.PMCode.Units
        dic['containersReceived'] = data.containersReceived

        dic["QC_No"] = PMgetQCNO()

        return Response(dic)


class PMSampleView(generics.CreateAPIView):
    queryset = PMSamples.objects.all()
    serializer_class = PMSampleSerializer


# Populate category model

class PopulateCategoryView(APIView):
    def get(self, request):
        workbook = pd.read_excel(r'C:\Users\usama riasat\Documents\s-clone\saff-apis\QualityAssurance\FormsQA.xlsx',
                                 sheet_name='Category')
        workbook = workbook.to_numpy()
        for i in workbook:
            cat = NCCategory.objects.create(
                category=i[0],
                subCategory=i[1]
            )
            cat.save()
        return Response({"Populate": "Done"})


# -------------------- NCR ------------------------

class AllUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = AllUsersSerializer(users, many=True)
        return Response(serializer.data)


class CategoriesView(APIView):
    def get(self, request):
        cat = NCCategory.objects.values_list('category').distinct()
        li = []
        for i in cat:
            dic = {}
            dic['category'] = i[0]
            li.append(dic)
        return Response(li)


class SubCategoriesView(APIView):
    def get(self, request, category):
        cat = NCCategory.objects.filter(category=category)
        serializer = SubCategoriesSerializer(cat, many=True)
        return Response(serializer.data)


class BatchNoView(APIView):
    def get(self, request, Pcode):
        bno = BPRLog.objects.filter(ProductCode=Pcode, batchStatus='OPEN')
        serializer = BatchNoSerializer(bno, many=True)
        return Response(serializer.data)


class HighestNCRView(APIView):
    def get(self, request):
        ncr1 = 0

        ncr1 = NCR.objects.aggregate(Max('NCRNo'))
        ncr1 = ncr1['NCRNo__max']
        if ncr1 is None:
            ncr1 = 0
        dic = {'NCRNo': ncr1}
        return Response(dic)


class NCRView(generics.CreateAPIView):
    queryset = NCR.objects.all()
    serializer_class = NCRSerializer


class NCRNoView(APIView):
    def get(self, request):
        ncrno = NCR.objects.all()
        serializer = NCRNoSerializer(ncrno, many=True)
        return Response(serializer.data)


class NCRDetailView(APIView):
    def get(self, request, NCRNo):
        nc = NCR.objects.get(NCRNo=NCRNo)
        dict = {}
        dict['date'] = nc.date
        dict['NCRNo'] = nc.NCRNo
        dict['status '] = nc.status
        dict['originator'] = nc.originator
        dict['section'] = nc.section
        dict['sourceOfIdentification'] = nc.sourceOfIdentification
        dict['refNo'] = nc.refNo
        dict['natureOfNC'] = nc.natureOfNC
        dict['gradeOfNC'] = nc.gradeOfNC
        dict['category'] = nc.category
        dict['subCategory'] = nc.subCategory
        dict['batchNo'] = nc.batchNo.batchNo
        dict['Product'] = nc.batchNo.ProductCode.Product
        dict['descriptionOFNonConformance'] = nc.descriptionOFNonConformance
        dict['solutionOfCurrentProblem'] = nc.solutionOfCurrentProblem
        dict['immediateAction'] = nc.immediateAction
        dict['isActionTaken'] = nc.isActionTaken
        dict['actionDate'] = nc.actionDate
        dict['verifiedBy'] = nc.verifiedBy
        dict['isLimitAction'] = nc.isLimitAction
        dict['rootCause'] = nc.rootCause
        dict['proposedCorrectiveAction'] = nc.proposedCorrectiveAction
        dict['actionTaken'] = nc.actionTaken
        return Response(dict)


# ------------------- NCR Close ---------------------#

class NCRNoStatusOpenView(APIView):
    def get(self, request):
        ncrno = NCR.objects.filter(status='OPEN')
        serializer = NCRNoSerializer(ncrno, many=True)
        return Response(serializer.data)


class CloseNCRView(generics.UpdateAPIView):
    queryset = NCR.objects.all()
    serializer_class = CloseNCRSerializer


# ------------------- Batch Close ---------------------#

class OpenBatchesView(APIView):
    def get(self, request):
        data = BPRLog.objects.filter(batchStatus='OPEN')
        serializer = BPRSerializer(data, many=True)
        return Response(serializer.data)


class CloseBPRView(generics.UpdateAPIView):
    queryset = BPRLog.objects.all()
    serializer_class = CloseBPRSerializer


#   -------------- Add Product --------------------

class ListOfDosageForms(APIView):
    def get(self, request):
        data = DosageForms.objects.all()
        l = []
        for i in data:
            dic = {}
            dic["dosageForm"] = i.dosageForm
            l.append(dic)
        return Response({"List": l})


class AddProductView(generics.CreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer


#   ---------------     View Product    ----------------------

class ProductCodeView(APIView):
    def get(self, request):
        pcode = Products.objects.all()
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class ProductDetailView(generics.ListAPIView):
    queryset = PackSizes.objects.all()
    serializer_class = ProductAndPackSizeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ProductCode__Product', 'ProductCode', 'ProductCode__RegistrationNo', 'ProductCode__ShelfLife']

    # -------------- Add RM --------------------


class RawMaterialView(generics.CreateAPIView):
    queryset = RawMaterials.objects.all()
    serializer_class = RawMaterialSerializer

    # -------------- View RM --------------------


class RawMaterialDetailView(generics.ListAPIView):
    queryset = RawMaterials.objects.all()
    serializer_class = RawMaterialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    # -------------- Add PM --------------------


class PackingMaterialView(generics.CreateAPIView):
    queryset = PackingMaterials.objects.all()
    serializer_class = PackingMaterialSerializer

    # -------------- View RM --------------------


class PackingMaterialDetailView(generics.ListAPIView):
    queryset = PackingMaterials.objects.all()
    serializer_class = PackingMaterialSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    # -------------- Batch Deviation ----------------


class HighestBDNoView(APIView):
    def get(self, request):
        bdno = 0
        bdno = BatchDeviation.objects.aggregate(Max('deviationNo'))
        bdno = bdno['deviationNo__max']
        if bdno is None:
            bdno = 0
        dic = {'deviationNo': bdno}
        return Response(dic)


class BatchDetailView(APIView):
    def get(self, request, batchNo):
        batch = BPRLog.objects.get(batchNo=batchNo)
        dic = {}
        dic['batchSize'] = batch.batchSize
        dic['MFGDate'] = batch.MFGDate
        dic['EXPDate'] = batch.EXPDate
        stages = Stages.objects.values_list('stage')
        li = []
        for i in stages:
            dict = {}
            dict['stage'] = i[0]
            li.append(dict)
        dic['stages'] = li
        return Response(dic)


class BatchDeviationView(generics.CreateAPIView):
    queryset = BatchDeviation.objects.all()
    serializer_class = BatchDeviationSerializer


# ------------ Print Batch Deviation -----------------#

class AllBDNoView(APIView):
    def get(self, request):
        bdno = BatchDeviation.objects.all()
        serializer = BatchDeviationNoSerializer(bdno, many=True)
        return Response(serializer.data)


class BatchDeviationDetailView(generics.RetrieveAPIView):
    queryset = BatchDeviation.objects.all()
    serializer_class = BatchDeviationSerializer


# --------------- Change Control -------------------#
class HighestCCNoView(APIView):
    def get(self, request):
        CCNo = 0

        CCNo = ChangeControl.objects.aggregate(Max('CCNo'))
        CCNo = CCNo['CCNo__max']
        if CCNo is None:
            CCNo = 0
        dic = {'CCNo': CCNo}
        return Response(dic)


# Print Change Control

class ChangeControlView(generics.CreateAPIView):
    queryset = ChangeControl.objects.all()
    serializer_class = ChangeControlSerializer


class ChangeControlNumbersListView(APIView):
    def get(self, request):
        data = ChangeControl.objects.all()
        l = []
        for i in data:
            l.append(i.CCNo)
        return Response(l)


class ChangeControlGetDataView(generics.RetrieveAPIView):
    queryset = ChangeControl.objects.all()
    serializer_class = ChangeControlSerializer


class changeControlVerificationOfChangesView(generics.UpdateAPIView):
    queryset = ChangeControl.objects.all()
    serializer_class = changeControlVerificationOfChangesSerialerzer


# -------------------------- Dispensation Request DRF ---------------------------#

class HighestDRFNoView(APIView):
    def get(self, request):
        DRFNo1 = 0

        DRFNo1 = DRF.objects.aggregate(Max('DRFNo'))
        DRFNo1 = DRFNo1['DRFNo__max']
        if DRFNo1 is None:
            DRFNo1 = 0
        dic = {'DRFNo1': DRFNo1}
        return Response(dic)

class DRFPostView(generics.CreateAPIView):
    serializer_class = DRFPostSerializer
    queryset = DRF.objects.all()

# -------------------------- Product Sample ---------------------------#

class PSPCodeView(APIView):
    def get(self, request):
        pcode = BPRLog.objects.filter(batchStatus='OPEN')
        l = []
        for i in pcode:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["ProductCode"] = i
            lis.append(dic)
        return Response(lis)


class PSBatchNoView(APIView):
    def get(self, request, Pcode):
        bno = BPRLog.objects.filter(ProductCode=Pcode, batchStatus='OPEN')
        serializer = BatchNoSerializer(bno, many=True)
        return Response(serializer.data)


class PSBatchDetailView(APIView):
    def get(self, request, batchNo):
        batch_detail = BPRLog.objects.get(batchNo=batchNo)
        dic = {}
        dic['MFGDate'] = batch_detail.MFGDate
        dic['EXPDate'] = batch_detail.EXPDate
        dic['currentStage'] = batch_detail.currentStage
        dic['batchSize'] = batch_detail.batchSize
        dic['QCNo'] = FPgetQCNO()
        return Response(dic)


class ProductSampleView(generics.CreateAPIView):
    queryset = ProductSamples.objects.all()
    serializer_class = ProductSampleSerializer


# ---------------- Batch Review -------------------#

class BRPCodeView(APIView):
    def get(self, request):
        pcode = BPRLog.objects.filter(batchStatus='UNDER_REVIEWED')
        serializer = PCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class BRBatchNoView(APIView):
    def get(self, request, Pcode):
        bno = BPRLog.objects.filter(ProductCode=Pcode, batchStatus='UNDER_REVIEWED')
        serializer = BatchNoSerializer(bno, many=True)
        return Response(serializer.data)


class BRBatchDetailView(APIView):
    def get(self, request, batchNo):
        batch_detail = BPRLog.objects.get(batchNo=batchNo)
        dic = {}
        dic['MFGDate'] = batch_detail.MFGDate
        dic['EXPDate'] = batch_detail.EXPDate
        dic['batchStatus'] = batch_detail.batchStatus
        dic['batchSize'] = batch_detail.batchSize
        dic['yieldPercentage'] = batch_detail.yieldPercentage
        dic['inProcess'] = batch_detail.inProcess
        dic['packed'] = batch_detail.packed
        return Response(dic)


class BRDetailView(APIView):
    serializer_class = BatchReviewSerializer

    def post(self, request):
        data = request.data
        batchNo = data['batchNo']
        remarks = data['remarks']
        permittedDispatch = data['permittedDispatch']
        dispatchPermission = data['dispatchPermission']
        checkNCRData = NCR.objects.filter(batchNo=batchNo)
        checkBDData = BatchDeviation.objects.filter(batchNo=batchNo)
        for checkNCR in checkNCRData:
            if checkNCR.status == 'OPEN':
                return Response({'message': 'NCR is not closed'}, status=status.HTTP_400_BAD_REQUEST)
        for checkBD in checkBDData:
            if checkBD.status == 'OPEN':
                return Response({'message': 'Batch Daviation is not closed'}, status=status.HTTP_400_BAD_REQUEST)
        dict = {}
        detail = BPRLog.objects.get(batchNo=batchNo)
        dict['Product'] = detail.ProductCode.Product
        dict['batchNo'] = batchNo
        dict['batchSize'] = detail.batchSize
        dict['MFGDate'] = detail.MFGDate
        dict['EXPDate'] = detail.EXPDate
        dict['batchStatus'] = permittedDispatch
        dict['dispatchPermission'] = dispatchPermission
        dict['remarks'] = remarks
        NCRNoList = []
        ncr = NCR.objects.filter(batchNo=batchNo).values_list('NCRNo')
        for i in ncr:
            dic = {}
            dic['NCRNo'] = i[0]
            NCRNoList.append(dic)
        dict['NCRNoList'] = NCRNoList
        BDNoList = []
        bd = BatchDeviation.objects.filter(batchNo=batchNo).values_list('deviationNo')
        for i in bd:
            dic = {}
            dic['deviationNo'] = i[0]
            BDNoList.append(dic)
        dict['BDNoList'] = BDNoList
        detail.batchStatus = permittedDispatch
        detail.save()
        bprlog = BPRLog.objects.get(batchNo=batchNo)
        br = BatchReview.objects.create(
            batchNo=bprlog,
            remarks=remarks,
            permittedDispatch=permittedDispatch,
            dispatchPermission=dispatchPermission,
        )
        return Response(dict)
