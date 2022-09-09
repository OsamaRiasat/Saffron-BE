from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd

from Production.models import Stages, BatchStages
from .models import *
from Inventory.models import RawMaterials
from .serializers import *
from Account.models import User
from django_filters.rest_framework import DjangoFilterBackend, filters


# ----------- SCRIPTS -----------------

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


class PopulatePMParametersView(APIView):
    def get(self, request):
        workbook = pd.read_excel(
            r'C:\Users\usama riasat\Documents\s-clone\saff-apis\QualityControl\parameters.xlsx ',
            sheet_name='Sheet2')
        workbook = workbook.to_numpy()

        for i in workbook:
            t = str(i[0])
            print(t)
            paramater1 = PMParameters.objects.create(parameter=i[0])
            paramater1.save()

        return Response({"Populate": "Done"})


class PopulateProductParametersView(APIView):
    def get(self, request):
        workbook = pd.read_excel(
            r'C:\Users\usama riasat\Documents\s-clone\saff-apis\QualityControl\parameters.xlsx ',
            sheet_name='Sheet3')
        workbook = workbook.to_numpy()

        for i in workbook:
            t = str(i[0])
            print(t)
            paramater1 = ProductParameters.objects.create(parameter=i[0])
            paramater1.save()

        return Response({"Populate": "Done"})


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     RAW MATERIALS     -----------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# --------------------- SPECIFICATIONS ------------------------


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


class RMCodeByNameForViewSpecsView(APIView):
    def get(self, request, RMName):
        rmcode = RawMaterials.objects.get(Material=RMName)
        serializer = RMCodeSerializer(rmcode)
        return Response(serializer.data)


class RMNameByRMCodeForViewSpecsView(APIView):
    def get(self, request, RMCode):
        rmcode = RawMaterials.objects.get(RMCode=RMCode)
        serializer = RMaterialSerializer(rmcode)
        return Response(serializer.data)


class RMViewSpecificationsView(APIView):
    def get(self, request, RMCode):
        data = {}
        spec = RMSpecifications.objects.get(RMCode=RMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
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
        li = RMSpecifications.objects.values_list('RMCode')
        pcode = RawMaterials.objects.exclude(RMCode__in=li)
        serializer = RMCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class RMCodeByNameView(APIView):
    def get(self, request, name):
        rmcode = RawMaterials.objects.get(Material=name)
        serializer = RMCodeSerializer(rmcode)
        return Response(serializer.data)


class RMaterialView(APIView):
    def get(self, request):
        # rm = RawMaterials.objects.all()
        # serializer = RMaterialSerializer(rm, many=True)
        li = RMSpecifications.objects.values_list('RMCode')
        rm = RawMaterials.objects.exclude(RMCode__in=li)
        serializer = RMaterialSerializer(rm, many=True)
        return Response(serializer.data)


class RMNameByRMCodeView(APIView):
    def get(self, request, RMCode):
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


# Edit RM Specs

class RMEditSpecsView(APIView):
    def get(self, request, RMCode):
        # rm=RawMaterials.objects.get(RMCode=RMCode)
        specs = RMSpecifications.objects.get(RMCode=RMCode)
        specs_items = RMSpecificationsItems.objects.filter(specID=specs)
        dict = {}
        dict['RMCode'] = specs.RMCode.RMCode
        dict['reference'] = specs.reference.reference
        dict['SOPNo'] = specs.SOPNo
        dict['date'] = specs.date.strftime("%d.%m.%Y")
        dict['version'] = specs.version
        lis = []
        for i in specs_items:
            dic = {}
            dic['parameter'] = i.parameter.parameter
            dic['specification'] = i.specification
            lis.append(dic)
        dict['items'] = lis

        return Response(dict)


class TEMPRMSpecificationsView(generics.CreateAPIView):
    queryset = TempRMSpecifications.objects.all()
    serializer_class = TempRMSpecificationsSerializer

    #         --------------    SAMPLE ASSIGNMENT   -----------


# RM Sample Assignment


class AnalystView(APIView):
    def get(self, request):
        analysts = User.objects.filter(role="QC_Analyst", is_active=True)
        print(analysts)
        serializer = AnalystSerializer(analysts, many=True)
        return Response(serializer.data)


class AnalystSampleView(APIView):
    def get(self, request, id):
        samples = RMSamples.objects.filter(analyst=id)
        dict = []
        for i in samples:
            dic = {}
            # name = i.IGPNo.RMCode.Material
            dic['QCNo'] = i.QCNo
            dic['Material'] = i.RMCode.Material
            dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y %H:%M")
            dic['status'] = i.status
            dict.append(dic)
        return Response(dict)


class RMQCNoListView(generics.ListAPIView):
    queryset = RMSamples.objects.all().only('QCNo')
    serializer_class = RMAnalysisQCNoSerializer


class RMSamplesView(APIView):
    def get(self, request):
        samples = RMSamples.objects.all()
        dict = []
        for i in samples:
            dic = {}
            dic['QCNo'] = i.QCNo
            # rm_receiving = RMReceiving.objects.get(IGPNo=i.IGPNo.IGPNo)
            # rm = RawMaterials.objects.get(RMCode=rm_receiving.RMCode.RMCode)
            dic['Date'] = i.samplingDateTime.strftime("%d.%m.%Y %H:%M")
            dic['Material'] = i.RMCode.Material
            dic['Unit'] = i.RMCode.Units
            dic['Quantity'] = i.quantityReceived
            try:
                dic['Analyst'] = i.analyst.username
                dic['AssigneDate'] = i.assignedDateTime.strftime(("%d.%m.%Y %H:%M"))
            except:
                dic['Analyst'] = "N/A"
                dic['AssigneDate'] = "N/A"

            dict.append(dic)
        return Response(dict)


class AssignAnalystView(generics.UpdateAPIView):
    queryset = RMSamples.objects.all()
    serializer_class = AssignAnalystSerializer

    # --------------------- Data Entry ------------------------


# RM Data Entry

class RMQCNoView(APIView):
    def get(self, request):
        user = request.user
        if (user.role == 'QC_Analyst'):
            qc = RMSamples.objects.filter(analyst=user.id)
            serializer = RMQCNoSerializer(qc, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'There is no QC sample for this Analyst'})


class RMQCNoSampleView(APIView):
    def get(self, request, QCNo):
        sample = RMSamples.objects.get(QCNo=QCNo)

        # rm_receiving = RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)

        dict = {}
        dict['samplingDateTime'] = sample.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        # dict['IGPNo'] = sample.IGPNo.IGPNo
        dict['IGPNo'] = 0
        dict['assignedDateTime'] = sample.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = sample.analyst.username

        dict['RMCode'] = sample.RMCode.RMCode
        dict['Material'] = sample.RMCode.Material
        dict['Units'] = sample.RMCode.Units
        dict['quantityReceived'] = sample.quantityReceived
        dict['batchNo'] = sample.batchNo
        dict['MFG_Date'] = sample.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = sample.EXP_Date.strftime("%d.%m.%Y")

        data = {}
        try:
            spec = RMSpecifications.objects.get(RMCode=sample.RMCode.RMCode)
        except:
            return Response({"message": "No Specifications for this Material"})
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
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
        dict['result'] = data
        return Response(dict)


class PostRMAnalysisView(generics.CreateAPIView):
    queryset = RMAnalysis.objects.all()
    serializer_class = PostRMAnalysisSerializer


# --------------------- COA APPROVAL ------------------------#

class RMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = RMAnalysis.objects.all()
        serializer = RMAnalysisQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class RMAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = RMAnalysis.objects.get(QCNo=QCNo)
        samples = RMSamples.objects.get(QCNo=QCNo)
        # rm_receiving = RMReceiving.objects.get(IGPNo=samples.IGPNo.IGPNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = samples.IGPNo
        dict['IGPNo'] = 0
        dict['RMCode'] = samples.RMCode.RMCode
        dict['Material'] = samples.RMCode.Material
        dict['Units'] = samples.RMCode.Units
        dict['quantityReceived'] = samples.quantityReceived
        dict['batchNo'] = samples.batchNo
        dict['MFG_Date'] = samples.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = samples.EXP_Date.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = RMSpecifications.objects.get(RMCode=samples.RMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference
        items = RMAnalysisItems.objects.filter(RMAnalysisID=analysis.RMAnalysisID)
        l = []
        for obj in items:
            spec_item = {}
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict['items'] = l
        return Response(dict)


class PostRMCOAApprovalView(APIView):
    serializer_class = RemarksSerializer

    def post(self, request, QCNo):
        data = request.data
        remarks = data.get('remarks', None)
        isRetest = data.get('isRetest', None)
        retestReason = data.get('retestReason', None)
        analysis = RMAnalysis.objects.get(QCNo=QCNo)
        retestDate = analysis.retestDate
        result = data.get('result', None)

        if result == "Reject":
            analysis = RMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = RMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=analysis.QCNo,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID,
                result="REJECTED"
            )
            log_analysis.save()
            analysis_items = RMAnalysisItems.objects.filter(RMAnalysisID=analysis.RMAnalysisID)
            for i in analysis_items:
                item = RMAnalysisItemsLog.objects.create(
                    RMAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            analysis.delete()

            sample = RMSamples.objects.get(QCNo=QCNo)
            sample.analyst = None
            sample.assignedDateTime = None
            sample.status = "PENDING"
            sample.save()
            # rm = RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
            # rm.quantityApproved = analysis.quantityApproved
            # rm.quantityRejected = analysis.quantityRejected
            # rm.QCNo = QCNo
            # rm.status = "REJECTED"
            # rm.retest_Date = retestDate
            # rm.save()
            return Response({"message": "Rejected"})
        else:
            sample = RMSamples.objects.get(QCNo=QCNo)
            analysis = RMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = RMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=sample,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID
            )
            log_analysis.save()
            analysis_items = RMAnalysisItems.objects.filter(RMAnalysisID=analysis.RMAnalysisID)
            for i in analysis_items:
                item = RMAnalysisItemsLog.objects.create(
                    RMAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            sample = RMSamples.objects.get(QCNo=QCNo)
            # rm = RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
            # rm.quantityApproved = analysis.quantityApproved
            # rm.quantityRejected = analysis.quantityRejected
            # rm.QCNo = QCNo
            # rm.status = "APPROVED"
            # rm.retest_Date = retestDate
            # rm.save()
            # sample.status = "APPROVED"
            # sample.result = "Released"
            # sample.save()
            # analysis.delete()
            return Response({"message": "Released"})


# class ReleaseRMAnalysisView(APIView):
#     serializer_class = RemarksSerializer
#
#     def post(self, request, QCNo):
#         data = request.data
#         remarks = data.get('remarks', None)


# --------------------- Data Analysis ------------------------


# Raw Materials
#
# class RMMaterialsListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMMaterialsListReportingSerializer
#
#
# class RMBatchNoListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMBatchNoListReportingSerializer


class RMDataAnalysisView(generics.ListAPIView):
    queryset = RMAnalysisItemsLog.objects.all()
    serializer_class = RMAnalysisItemsReportingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['RMAnalysisID__QCNo__RMCode__Material',
                        'RMAnalysisID__QCNo__batchNo',
                        'RMAnalysisID__QCNo__QCNo',
                        'parameter',
                        'RMAnalysisID__QCNo__S_ID__S_Name']
    #         --------------    ANALYST MANAGEMENT  -----------


class BlockUnBlockAnalystView(APIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        check = ''
        if user.is_active == True:
            user.is_active = False
            check = "Blocked"
        else:
            user.is_active = True
            check = "UnBlock"
        user.save()
        return Response({'message': check})


class AllAnalystView(APIView):
    def get(self, request):
        user = User.objects.filter(role='QC_Analyst')
        dict = []
        for i in user:
            dic = {}
            dic['id'] = i.id
            dic['username'] = i.username
            if i.is_active == False:
                dic['status'] = 'Blocked'
            else:
                dic['status'] = 'UnBlock'
            dict.append(dic)
        return Response(dict)

    # -------------- ANALYST LOGIN -------------


#   Pending RM Samples

class CurrentAnalystSampleView(APIView):
    def get(self, request):
        user = request.user
        if user.role == 'QC_Analyst':
            samples = RMSamples.objects.filter(analyst=user.id, status="ASSIGNED")
            dict = []
            for i in samples:
                dic = {}
                # name = i.IGPNo.RMCode.Material
                dic['QCNo'] = i.QCNo
                dic['Material'] = i.RMCode.Material
                dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y")
                dict.append(dic)
            return Response(dict)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# --------------------- Pending Reports ------------------------#

class Print_RMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = RMAnalysisLog.objects.filter(isPrinted=False)
        serializer = RMAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class Print_RMAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = RMAnalysisLog.objects.get(QCNo=QCNo)
        samples = RMSamples.objects.get(QCNo=QCNo)
        # rm_receiving = RMReceiving.objects.get(IGPNo=samples.IGPNo.IGPNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        # dict['IGPNo'] = samples.IGPNo
        dict['IGPNo'] = 0
        dict['containersReceived'] = samples.containersReceived
        dict['S_Name'] = samples.S_ID.S_Name
        dict['RMCode'] = samples.RMCode.RMCode
        dict['Material'] = samples.RMCode.Material
        dict['Units'] = samples.RMCode.Units
        dict['quantityReceived'] = samples.quantityReceived
        dict['batchNo'] = samples.batchNo
        dict['MFG_Date'] = samples.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = samples.EXP_Date.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['result'] = analysis.result
        dict['remarks'] = analysis.remarks
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = RMSpecifications.objects.get(RMCode=samples.RMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference
        items = RMAnalysisItemsLog.objects.filter(RMAnalysisID=analysis.RMAnalysisID)
        l = []
        assay="Nil"
        for obj in items:
            spec_item = {}
            if obj.parameter=="Assay":
                assay=obj.result
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict["Assay"] = assay
        dict['items'] = l
        return Response(dict)


class RMAnalysisLogPrintView(APIView):
    def get(self, request, qc):
        dev = RMAnalysisLog.objects.filter(QCNo=qc).first()
        dev.isPrinted = True
        dev.save()
        print(dev.isPrinted)
        return Response({"message": "Printed Successfully"})


# --------------------- Label Printing ------------------------#

class Label_Print_RMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = RMAnalysisLog.objects.all()
        serializer = RMAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PACKING MATERIALS     ---------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# --------------------- SPECIFICATIONS ------------------------


# View Specs

class PMCodeListOfSpecificationsView(generics.ListAPIView):
    queryset = PMSpecifications.objects.only('PMCode').filter(QAStatus="ALLOWED")
    serializer_class = AcquirePMCodeListSerializer


class PMMaterialListOfSpecificationsView(APIView):
    def get(self, request):
        pm = PMSpecifications.objects.only('PMCode').filter(QAStatus="ALLOWED")
        li = []
        for i in pm:
            dic = {}
            dic['Material'] = i.PMCode.Material
            li.append(dic)
        return Response(li)


class PMCodeByNameForViewSpecsView(APIView):
    def get(self, request, PMName):
        pmcode = PackingMaterials.objects.get(Material=PMName)
        serializer = PMCodeSerializer(pmcode)
        return Response(serializer.data)


class PMNameByPMCodeForViewSpecsView(APIView):
    def get(self, request, PMCode):
        pmcode = PackingMaterials.objects.get(PMCode=PMCode)
        serializer = PMaterialSerializer(pmcode)
        return Response(serializer.data)


class PMViewSpecificationsView(APIView):
    def get(self, request, PMCode):
        data = {}
        spec = PMSpecifications.objects.get(PMCode=PMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = PMSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        return Response(data)


# New Specs

class PMCodeView(APIView):
    def get(self, request):
        li = PMSpecifications.objects.values_list('PMCode')
        pmcode = PackingMaterials.objects.exclude(PMCode__in=li)
        # pmcode = PackingMaterials.objects.all()
        serializer = PMCodeSerializer(pmcode, many=True)
        return Response(serializer.data)


class PMCodeByNameView(APIView):
    def get(self, request, name):
        pmcode = PackingMaterials.objects.get(Material=name)
        serializer = PMCodeSerializer(pmcode)
        return Response(serializer.data)


class PMaterialView(APIView):
    def get(self, request):
        li = PMSpecifications.objects.values_list('PMCode')
        pm = PackingMaterials.objects.exclude(PMCode__in=li)
        # pm = PackingMaterials.objects.all()
        serializer = PMaterialSerializer(pm, many=True)
        return Response(serializer.data)


class PMNameByPMCodeView(APIView):
    def get(self, request, PMCode):
        pmcode = PackingMaterials.objects.get(PMCode=PMCode)
        serializer = PMaterialSerializer(pmcode)
        return Response(serializer.data)


#
# class RMReferenceView(APIView):
#     def get(self, request):
#         ref = RMReferences.objects.all()
#         serializer = RMReferencesSerializer(ref, many=True)
#         return Response(serializer.data)


class PMParametersView(APIView):
    def get(self, request):
        ref = PMParameters.objects.all()
        serializer = PMParameterSerializer(ref, many=True)
        return Response(serializer.data)


class PMSpecificationsView(generics.CreateAPIView):
    queryset = PMSpecifications.objects.all()
    serializer_class = PMSpecificationsSerializer


class PMAcquireSpecificationsView(APIView):
    def get(self, request, PMCode):
        spec = PMSpecifications.objects.get(PMCode=PMCode)
        spec_items = PMSpecificationsItems.objects.filter(specID=spec)
        serializer = PMAcquireSpecificationsItemsSerializer(spec_items, many=True)
        return Response(serializer.data)


class AcquirePMCodeListView(generics.ListAPIView):
    queryset = PMSpecifications.objects.all()
    serializer_class = AcquirePMCodeListSerializer


class AcquirePMaterialListView(APIView):
    def get(self, request):
        rm = PMSpecifications.objects.all()
        li = []
        for i in rm:
            dic = {}
            dic['Material'] = i.PMCode.Material
            li.append(dic)
        return Response(li)


# Edit PM Specs

class PMEditSpecsView(APIView):
    def get(self, request, PMCode):
        # rm=RawMaterials.objects.get(RMCode=RMCode)
        specs = PMSpecifications.objects.get(PMCode=PMCode)
        specs_items = PMSpecificationsItems.objects.filter(specID=specs)
        dict = {}
        dict['RMCode'] = specs.PMCode.PMCode
        dict['reference'] = specs.reference.reference
        dict['SOPNo'] = specs.SOPNo
        dict['date'] = specs.date.strftime("%d.%m.%Y")
        dict['version'] = specs.version
        lis = []
        for i in specs_items:
            dic = {}
            dic['parameter'] = i.parameter.parameter
            dic['specification'] = i.specification
            lis.append(dic)
        dict['items'] = lis
        return Response(dict)


class TEMPPMSpecificationsView(generics.CreateAPIView):
    queryset = TempPMSpecifications.objects.all()
    serializer_class = TempPMSpecificationsSerializer

    #         --------------    SAMPLE ASSIGNMENT   -----------


# PM Sample Assignment

#
# class PMAnalystView(APIView):
#     def get(self, request):
#         analysts = User.objects.filter(role="QC_Analyst", is_active=True)
#         print(analysts)
#         serializer = AnalystSerializer(analysts, many=True)
#         return Response(serializer.data)


class PMAnalystSampleView(APIView):
    def get(self, request, id):
        samples = PMSamples.objects.filter(analyst=id)
        dict = []
        for i in samples:
            dic = {}
            name = i.IGPNo.PMCode.Material
            dic['QCNo'] = i.QCNo
            dic['Material'] = name
            dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y %H:%M")
            dic['status'] = i.status
            dict.append(dic)
        return Response(dict)


class PMQCNoListView(generics.ListAPIView):
    queryset = PMSamples.objects.all().only('QCNo')
    serializer_class = PMAnalysisQCNoSerializer


class PMSamplesView(APIView):
    def get(self, request):
        samples = PMSamples.objects.all()
        dict = []
        for i in samples:
            dic = {}
            dic['QCNo'] = i.QCNo
            pm_receiving = PMReceiving.objects.get(IGPNo=i.IGPNo.IGPNo)
            pm = PackingMaterials.objects.get(PMCode=pm_receiving.PMCode.PMCode)
            dic['Date'] = i.samplingDateTime.strftime("%d.%m.%Y %H:%M")
            dic['Material'] = pm.Material
            dic['Unit'] = pm.Units
            dic['Quantity'] = pm_receiving.quantityReceived
            try:
                dic['Analyst'] = i.analyst.username
                dic['AssigneDate'] = i.assignedDateTime.strftime(("%d.%m.%Y %H:%M"))
            except:
                dic['Analyst'] = "N/A"
                dic['AssigneDate'] = "N/A"

            dict.append(dic)
        return Response(dict)


class PMAssignAnalystView(generics.UpdateAPIView):
    queryset = PMSamples.objects.all()
    serializer_class = PMAssignAnalystSerializer

    # --------------------- Data Entry ------------------------


# PM Data Entry

class PMQCNoView(APIView):
    def get(self, request):
        user = request.user
        if (user.role == 'QC_Analyst'):
            qc = PMSamples.objects.filter(analyst=user.id, status="ASSIGNED")
            serializer = PMQCNoSerializer(qc, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'There is no QC sample for this Analyst'})


class PMQCNoSampleView(APIView):
    def get(self, request, QCNo):
        sample = PMSamples.objects.get(QCNo=QCNo)

        pm_receiving = PMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)

        dict = {}
        dict['samplingDateTime'] = sample.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = sample.IGPNo.IGPNo
        dict['assignedDateTime'] = sample.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = sample.analyst.username

        dict['RMCode'] = pm_receiving.PMCode.PMCode
        dict['Material'] = pm_receiving.PMCode.Material
        dict['Units'] = pm_receiving.PMCode.Units
        dict['quantityReceived'] = pm_receiving.quantityReceived
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXP_Date.strftime("%d.%m.%Y")

        data = {}
        try:
            spec = PMSpecifications.objects.get(PMCode=pm_receiving.PMCode.PMCode)
        except:
            return Response({"message": "No Specifications for this Material"})
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = PMSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        dict['result'] = data
        return Response(dict)


class PostPMAnalysisView(generics.CreateAPIView):
    queryset = PMAnalysis.objects.all()
    serializer_class = PostPMAnalysisSerializer


# --------------------- COA APPROVAL ------------------------#

class PMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = PMAnalysis.objects.all()
        serializer = PMAnalysisQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class PMAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = PMAnalysis.objects.get(QCNo=QCNo)
        samples = PMSamples.objects.get(QCNo=QCNo)
        pm_receiving = PMReceiving.objects.get(IGPNo=samples.IGPNo.IGPNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = pm_receiving.IGPNo
        dict['RMCode'] = pm_receiving.PMCode.PMCode
        dict['Material'] = pm_receiving.PMCode.Material
        dict['Units'] = pm_receiving.PMCode.Units
        dict['quantityReceived'] = pm_receiving.quantityReceived
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXP_Date.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = PMSpecifications.objects.get(PMCode=pm_receiving.PMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference

        items = PMAnalysisItems.objects.filter(PMAnalysisID=analysis.PMAnalysisID)
        l = []
        for obj in items:
            spec_item = {}
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict['items'] = l
        return Response(dict)


class PostPMCOAApprovalView(APIView):
    serializer_class = RemarksSerializer

    def post(self, request, QCNo):
        data = request.data
        remarks = data.get('remarks', None)
        isRetest = data.get('isRetest', None)
        retestReason = data.get('retestReason', None)
        analysis = PMAnalysis.objects.get(QCNo=QCNo)
        retestDate = analysis.retestDate
        result = data.get('result', None)

        if result == "Reject":
            analysis = PMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = PMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=analysis.QCNo,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID,
                result="REJECTED"
            )
            log_analysis.save()
            analysis_items = PMAnalysisItems.objects.filter(PMAnalysisID=analysis.PMAnalysisID)
            for i in analysis_items:
                item = PMAnalysisItemsLog.objects.create(
                    PMAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            analysis.delete()
            sample = PMSamples.objects.get(QCNo=QCNo)
            pm = PMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
            pm.quantityApproved = analysis.quantityApproved
            pm.quantityRejected = analysis.quantityRejected
            pm.QCNo = QCNo
            pm.status = "REJECTED"
            pm.retest_Date = retestDate
            pm.save()
            sample.analyst = None
            sample.assignedDateTime = None
            sample.status = "PENDING"
            sample.save()
            return Response({"message": "Rejected"})
        else:
            sample = PMSamples.objects.get(QCNo=QCNo)
            analysis = PMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = PMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=sample,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID
            )
            log_analysis.save()
            analysis_items = PMAnalysisItems.objects.filter(PMAnalysisID=analysis.PMAnalysisID)
            for i in analysis_items:
                item = PMAnalysisItemsLog.objects.create(
                    PMAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            sample = PMSamples.objects.get(QCNo=QCNo)
            pm = PMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
            pm.quantityApproved = analysis.quantityApproved
            pm.quantityRejected = analysis.quantityRejected
            pm.QCNo = QCNo
            pm.status = "APPROVED"
            pm.retest_Date = retestDate
            pm.save()
            sample.status = "APPROVED"
            sample.result = "Released"
            sample.save()
            analysis.delete()
            return Response({"message": "Released"})


# --------------------- Pending Reports ------------------------#

class Print_PMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = PMAnalysisLog.objects.filter(isPrinted=False)
        serializer = PMAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class Print_PMAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = PMAnalysisLog.objects.get(QCNo=QCNo)
        samples = PMSamples.objects.get(QCNo=QCNo)
        pm_receiving = PMReceiving.objects.get(IGPNo=samples.IGPNo.IGPNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = pm_receiving.IGPNo
        dict['containersReceived'] = pm_receiving.containersReceived
        dict['S_Name'] = pm_receiving.S_ID.S_Name
        dict['RMCode'] = pm_receiving.PMCode.PMCode
        dict['Material'] = pm_receiving.PMCode.Material
        dict['Units'] = pm_receiving.PMCode.Units
        dict['quantityReceived'] = pm_receiving.quantityReceived
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXP_Date.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['result'] = analysis.result
        dict['remarks'] = analysis.remarks
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = PMSpecifications.objects.get(PMCode=pm_receiving.PMCode)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference

        items = PMAnalysisItemsLog.objects.filter(PMAnalysisID=analysis.PMAnalysisID)
        l = []
        assay = "Nil"
        for obj in items:
            spec_item = {}
            if obj.parameter == "Assay":
                assay = obj.result
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict["Assay"] = assay
        dict['items'] = l
        return Response(dict)


class PMAnalysisLogPrintView(APIView):
    # serializer_class = PMAnalysisLogPrintSerializer
    # queryset = PMAnalysisLog.objects.all()
    def get(self, request, qc):
        dev = PMAnalysisLog.objects.filter(QCNo=qc).first()
        dev.isPrinted = True
        dev.save()
        return Response()


# --------------------- Label Printing ------------------------#

class Label_Print_PMAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = PMAnalysisLog.objects.all()
        serializer = PMAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)

# --------------------- Data Analysis ------------------------


# Raw Materials
#
# class RMMaterialsListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMMaterialsListReportingSerializer
#
#
# class RMBatchNoListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMBatchNoListReportingSerializer


class PMDataAnalysisView(generics.ListAPIView):
    queryset = PMAnalysisItemsLog.objects.all()
    serializer_class = PMAnalysisItemsReportingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['PMAnalysisID__QCNo__PMCode__Material',
                        'PMAnalysisID__QCNo__batchNo',
                        'PMAnalysisID__QCNo__QCNo',
                        'parameter',
                        'PMAnalysisID__QCNo__S_ID__S_Name']
    # -------------- ANALYST LOGIN -------------


#   Pending RM Samples

class PMCurrentAnalystSampleView(APIView):
    def get(self, request):
        user = request.user
        if user.role == 'QC_Analyst':
            samples = PMSamples.objects.filter(analyst=user.id, status="ASSIGNED")
            dict = []
            for i in samples:
                dic = {}
                name = i.IGPNo.PMCode.Material
                dic['QCNo'] = i.QCNo
                dic['Material'] = name
                dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y")
                dict.append(dic)
            return Response(dict)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------     PRODUCTS     ----------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


# --------------------- SPECIFICATIONS ------------------------


# View Specs

class ProductCodeListOfSpecificationsView(APIView):
    # queryset = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
    # serializer_class = AcquireProductCodeListSerializer
    def get(self, request):
        data = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
        l = []
        for i in data:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["ProductCode"] = i
            lis.append(dic)
        return Response(lis)


class ProductStageListOfSpecificationsView(APIView):
    # queryset = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
    # serializer_class = AcquireProductCodeListSerializer
    def get(self, request, ProductCode):
        data = ProductSpecifications.objects.only('stage').filter(QAStatus="ALLOWED", ProductCode=ProductCode)
        l = []
        for i in data:
            l.append(i.stage)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["stage"] = i
            lis.append(dic)
        return Response(lis)


class ProductListOfSpecificationsView(APIView):
    def get(self, request):
        data = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
        l = []
        for i in data:
            l.append(i.ProductCode.Product)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["Product"] = i
            lis.append(dic)
        return Response(lis)


class ProductCodeByNameForViewSpecsView(APIView):
    def get(self, request, Product):
        productcode = Products.objects.get(Product=Product)
        serializer = ProductCodeSerializer(productcode)
        return Response(serializer.data)


class ProductNameByProductCodeForViewSpecsView(APIView):
    def get(self, request, ProductCode):
        pcode = Products.objects.get(ProductCode=ProductCode)
        serializer = ProductSerializer(pcode)
        return Response(serializer.data)


class ProductViewSpecificationsView(APIView):
    def get(self, request, ProductCode, stage):
        data = {}
        spec = ProductSpecifications.objects.get(ProductCode=ProductCode, stage=stage)
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = ProductSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        return Response(data)


# New Specs

class ProductCodeView(APIView):
    def get(self, request):
        pcode = Products.objects.only('ProductCode').all()
        serializer = ProductCodeSerializer(pcode, many=True)
        return Response(serializer.data)


class StageByPCodeView(APIView):
    # queryset = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
    # serializer_class = AcquireProductCodeListSerializer
    def get(self, request, ProductCode):
        product = Products.objects.get(ProductCode=ProductCode)
        li = ProductSpecifications.objects.filter(ProductCode=ProductCode).values_list('stage')
        stages = Stages.objects.exclude(stage__in=li, dosageForm=product.dosageForm.dosageForm)
        lis = []
        for i in stages:
            dic = {}
            dic["stage"] = i.stage
            lis.append(dic)
        return Response(lis)


class ProductCodeByNameView(APIView):
    def get(self, request, name):
        pcode = Products.objects.get(Product=name)
        serializer = ProductCodeSerializer(pcode)
        return Response(serializer.data)


class ProductView(APIView):
    def get(self, request):
        rm = Products.objects.only('Product').all()
        serializer = ProductSerializer(rm, many=True)
        return Response(serializer.data)


class ProductNameByProductCodeView(APIView):
    def get(self, request, ProductCode):
        pcode = Products.objects.get(ProductCode=ProductCode)
        serializer = ProductSerializer(pcode)
        return Response(serializer.data)


#
# class RMReferenceView(APIView):
#     def get(self, request):
#         ref = RMReferences.objects.all()
#         serializer = RMReferencesSerializer(ref, many=True)
#         return Response(serializer.data)


class ProductParametersView(APIView):
    def get(self, request):
        ref = ProductParameters.objects.all()
        serializer = ProductParameterSerializer(ref, many=True)
        return Response(serializer.data)


class ProductSpecificationsView(generics.CreateAPIView):
    queryset = ProductSpecifications.objects.all()
    serializer_class = ProductSpecificationsSerializer


class ProductAcquireSpecificationsView(APIView):
    def get(self, request, ProductCode, stage):
        spec = ProductSpecifications.objects.get(ProductCode=ProductCode, stage=stage)
        spec_items = ProductSpecificationsItems.objects.filter(specID=spec)
        serializer = ProductAcquireSpecificationsItemsSerializer(spec_items, many=True)
        return Response(serializer.data)


class AcquireProductCodeListView(APIView):
    def get(self, request):
        data = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
        l = []
        for i in data:
            l.append(i.ProductCode.ProductCode)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["ProductCode"] = i
            lis.append(dic)
        return Response(lis)


class AcquireProductListView(APIView):
    def get(self, request):
        data = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
        l = []
        for i in data:
            l.append(i.ProductCode.Product)
        l = list(dict.fromkeys(l))
        lis = []
        for i in l:
            dic = {}
            dic["Product"] = i
            lis.append(dic)
        return Response(lis)


# Edit PM Specs

class AllStageByPCodeView(APIView):
    # queryset = ProductSpecifications.objects.only('ProductCode').filter(QAStatus="ALLOWED")
    # serializer_class = AcquireProductCodeListSerializer
    def get(self, request, ProductCode):
        product = Products.objects.get(ProductCode=ProductCode)
        stages = Stages.objects.filter(dosageForm=product.dosageForm.dosageForm)
        lis = []
        for i in stages:
            dic = {}
            dic["stage"] = i.stage
            lis.append(dic)
        return Response(lis)


class ProductEditSpecsView(APIView):
    def get(self, request, ProductCode, stage):
        # rm=RawMaterials.objects.get(RMCode=RMCode)
        specs = ProductSpecifications.objects.get(ProductCode=ProductCode, stage=stage)
        specs_items = ProductSpecificationsItems.objects.filter(specID=specs)
        dict = {}
        dict['ProductCode'] = specs.ProductCode.ProductCode
        dict['stage'] = specs.stage
        dict['reference'] = specs.reference.reference
        dict['SOPNo'] = specs.SOPNo
        dict['date'] = specs.date.strftime("%d.%m.%Y")
        dict['version'] = specs.version
        lis = []
        for i in specs_items:
            dic = {}
            dic['parameter'] = i.parameter.parameter
            dic['specification'] = i.specification
            lis.append(dic)
        dict['items'] = lis
        return Response(dict)


class TEMPProductSpecificationsView(generics.CreateAPIView):
    queryset = TempProductSpecifications.objects.all()
    serializer_class = TempProductSpecificationsSerializer

    #         --------------    SAMPLE ASSIGNMENT   -----------


# PM Sample Assignment


# class PMAnalystView(APIView):
#     def get(self, request):
#         analysts = User.objects.filter(role="QC_Analyst", is_active=True)
#         print(analysts)
#         serializer = AnalystSerializer(analysts, many=True)
#         return Response(serializer.data)


class ProductAnalystSampleView(APIView):
    def get(self, request, id):
        samples = ProductSamples.objects.filter(analyst=id)
        dict = []
        for i in samples:
            dic = {}
            name = i.batchNo.ProductCode.Product
            dic['QCNo'] = i.QCNo
            dic['Product'] = name
            dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y %H:%M")
            dic['status'] = i.status
            dic['stage'] = i.sampleStage
            dict.append(dic)
        return Response(dict)


class ProductQCNoListView(generics.ListAPIView):
    queryset = ProductSamples.objects.all().only('QCNo')
    serializer_class = ProductAnalysisQCNoSerializer


class ProductSamplesView(APIView):
    def get(self, request):
        samples = ProductSamples.objects.all()
        dict = []
        for i in samples:
            dic = {}
            dic['QCNo'] = i.QCNo
            pm_receiving = BPRLog.objects.get(batchNo=i.batchNo.batchNo)
            pm = Products.objects.get(ProductCode=pm_receiving.ProductCode.ProductCode)
            dic['Date'] = i.samplingDateTime.strftime("%d.%m.%Y %H:%M")
            dic['Product'] = pm.Product
            dic['Unit'] = i.sampleUnity
            dic['Quantity'] = pm_receiving.batchSize
            dic['stage'] = i.sampleStage
            try:
                dic['Analyst'] = i.analyst.username
                dic['AssigneDate'] = i.assignedDateTime.strftime(("%d.%m.%Y %H:%M"))
            except:
                dic['Analyst'] = "N/A"
                dic['AssigneDate'] = "N/A"

            dict.append(dic)
        return Response(dict)


class ProductAssignAnalystView(generics.UpdateAPIView):
    queryset = ProductSamples.objects.all()
    serializer_class = ProductAssignAnalystSerializer

    # --------------------- Data Entry ------------------------


# PM Data Entry

class ProductQCNoView(APIView):
    def get(self, request):
        user = request.user
        if (user.role == 'QC_Analyst'):
            qc = ProductSamples.objects.filter(analyst=user.id, status="ASSIGNED")
            serializer = ProductQCNoSerializer(qc, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'There is no QC sample for this Analyst'})


class ProductQCNoSampleView(APIView):
    def get(self, request, QCNo):
        sample = ProductSamples.objects.get(QCNo=QCNo)

        pm_receiving = BPRLog.objects.get(batchNo=sample.batchNo.batchNo)
        units = ""
        try:
            lastStage = BatchStages.objects.filter(batchNo=sample.batchNo.batchNo,
                                                   currentStage=sample.sampleStage).first()
            for i in lastStage:
                units = i.units
        except:
            units = "Numbers"
        dict = {}
        dict['samplingDateTime'] = sample.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['batchNo'] = sample.batchNo.batchNo
        dict['assignedDateTime'] = sample.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = sample.analyst.username

        dict['ProductCode'] = pm_receiving.ProductCode.ProductCode
        dict['Product'] = pm_receiving.ProductCode.Product
        dict['Units'] = sample.sampleUnity
        dict['quantityReceived'] = pm_receiving.batchSize
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFGDate.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXPDate.strftime("%d.%m.%Y")

        data = {}
        print("Holl", sample.sampleStage)
        spec = ProductSpecifications.objects.get(ProductCode=pm_receiving.ProductCode.ProductCode,
                                                 stage=sample.sampleStage)
        print(spec)
        try:
            spec = ProductSpecifications.objects.get(ProductCode=pm_receiving.ProductCode.ProductCode,
                                                     stage=sample.sampleStage)
        except:
            return Response({
                                "message": "Add Specifications for " + sample.batchNo.ProductCode.Product + "for stage " + sample.sampleStage + " first."})
        str1 = spec.SOPNo + " Version:" + str(spec.version) + " Date:" + str(spec.date.strftime('%d-%m-%Y'))
        data["FirstData"] = str1
        data["SecondData"] = spec.reference.reference
        spec_items = ProductSpecificationsItems.objects.filter(specID=spec)
        l = []
        for obj in spec_items:
            spec_item = {}
            spec_item["paramater"] = obj.parameter.parameter
            spec_item["specification"] = obj.specification
            l.append(spec_item)
        data["list"] = l
        dict['result'] = data
        return Response(dict)


class PostProductAnalysisView(generics.CreateAPIView):
    queryset = ProductAnalysis.objects.all()
    serializer_class = PostProductAnalysisSerializer


# --------------------- COA APPROVAL ------------------------#

class ProductAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = ProductAnalysis.objects.all()
        serializer = ProductAnalysisQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class ProductAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = ProductAnalysis.objects.get(QCNo=QCNo)
        samples = ProductSamples.objects.get(QCNo=QCNo)
        units = ""
        try:
            lastStage = BatchStages.objects.filter(batchNo=samples.batchNo.batchNo,
                                                   currentStage=samples.sampleStage).first()
            for i in lastStage:
                units = i.units
        except:
            units = "Numbers"
        pm_receiving = BPRLog.objects.get(batchNo=samples.batchNo.batchNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['batchNo'] = pm_receiving.batchNo
        dict['ProductCode'] = pm_receiving.ProductCode.ProductCode
        dict['Product'] = pm_receiving.ProductCode.Product
        dict['Units'] = samples.sampleUnity
        dict['quantityReceived'] = samples.sampleQuantity  # No
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFGDate.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXPDate.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = ProductSpecifications.objects.get(ProductCode=pm_receiving.ProductCode, stage=samples.sampleStage)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference

        items = ProductAnalysisItems.objects.filter(ProductAnalysisID=analysis.ProductAnalysisID)
        l = []
        for obj in items:
            spec_item = {}
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict['items'] = l
        return Response(dict)


class PostProductCOAApprovalView(APIView):
    serializer_class = RemarksSerializer

    def post(self, request, QCNo):
        data = request.data
        remarks = data.get('remarks', None)
        isRetest = data.get('isRetest', None)
        retestReason = data.get('retestReason', None)
        analysis = ProductAnalysis.objects.get(QCNo=QCNo)
        retestDate = analysis.retestDate
        result = data.get('result', None)

        if result == "Reject":
            analysis = ProductAnalysis.objects.get(QCNo=QCNo)
            log_analysis = ProductAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=analysis.QCNo,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID,
                result="REJECTED"
            )
            log_analysis.save()
            analysis_items = ProductAnalysisItems.objects.filter(ProductAnalysisID=analysis.ProductAnalysisID)
            for i in analysis_items:
                item = ProductAnalysisItemsLog.objects.create(
                    ProductAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            analysis.delete()
            sample = ProductSamples.objects.get(QCNo=QCNo)
            sample.analyst = None
            sample.assignedDateTime = None
            sample.status = "PENDING"
            sample.save()
            return Response({"message": "Rejected"})
        else:
            sample = ProductSamples.objects.get(QCNo=QCNo)
            analysis = ProductAnalysis.objects.get(QCNo=QCNo)
            log_analysis = ProductAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=sample,
                analysisDateTime=analysis.analysisDateTime,
                retestDate=analysis.retestDate,
                quantityApproved=analysis.quantityApproved,
                quantityRejected=analysis.quantityRejected,
                remarks=remarks,
                specID=analysis.specID
            )
            log_analysis.save()
            analysis_items = ProductAnalysisItems.objects.filter(ProductAnalysisID=analysis.ProductAnalysisID)
            for i in analysis_items:
                item = ProductAnalysisItemsLog.objects.create(
                    ProductAnalysisID=log_analysis,
                    parameter=i.parameter,
                    specification=i.specification,
                    result=i.result
                )
                item.save()
            sample = ProductSamples.objects.get(QCNo=QCNo)
            # pm = BPRLog.objects.get(batchNo=sample.batchNo.batchNo)
            # pm.quantityApproved = analysis.quantityApproved
            # pm.quantityRejected = analysis.quantityRejected
            # pm.QCNo = QCNo
            # pm.status = "APPROVED"
            # pm.retest_Date = retestDate
            # pm.save()
            sample.status = "APPROVED"
            sample.result = "Released"
            sample.save()
            analysis.delete()
            return Response({"message": "Released"})


# --------------------- Pending Reports ------------------------#

class Print_ProductAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = ProductAnalysisLog.objects.filter(isPrinted=False)
        serializer = ProductAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)


class Print_ProductAnalysisView(APIView):
    def get(self, request, QCNo):
        analysis = ProductAnalysisLog.objects.get(QCNo=QCNo)
        samples = ProductSamples.objects.get(QCNo=QCNo)
        units = ""
        try:
            lastStage = BatchStages.objects.filter(batchNo=samples.batchNo.batchNo,
                                                   currentStage=samples.sampleStage).first()
            for i in lastStage:
                units = i.units
        except:
            units = "Numbers"
        pm_receiving = BPRLog.objects.get(batchNo=samples.batchNo.batchNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['batchNo'] = pm_receiving.batchNo
        dict['ProductCode'] = pm_receiving.ProductCode.ProductCode
        dict['Product'] = pm_receiving.ProductCode.Product
        dict['Units'] = samples.sampleUnity
        dict['quantityReceived'] = samples.sampleQuantity  # No
        dict['batchNo'] = pm_receiving.batchNo
        dict['MFG_Date'] = pm_receiving.MFGDate.strftime("%d.%m.%Y")
        dict['EXP_Date'] = pm_receiving.EXPDate.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['result'] = analysis.result
        dict['remarks'] = analysis.remarks
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username

        spec = ProductSpecifications.objects.get(ProductCode=pm_receiving.ProductCode, stage=samples.sampleStage)
        str1 = spec.SOPNo + " Version:" + str(spec.version)
        dict["FirstData"] = str1
        dict["SecondData"] = spec.reference.reference

        items = ProductAnalysisItemsLog.objects.filter(ProductAnalysisID=analysis.ProductAnalysisID)
        l = []
        for obj in items:
            spec_item = {}
            spec_item["parameter"] = obj.parameter
            spec_item["specification"] = obj.specification
            spec_item["result"] = obj.result
            l.append(spec_item)
        dict['items'] = l
        return Response(dict)


class ProductAnalysisLogPrintView(APIView):
    def get(self, request, qc):
        dev = ProductAnalysisLog.objects.filter(QCNo=qc).first()
        dev.isPrinted = True
        dev.save()
        return Response()


# --------------------- Label Printing ------------------------#

class Label_Print_ProductAnalysisQCNoView(APIView):
    def get(self, request):
        qcno = ProductAnalysisLog.objects.all()
        serializer = ProductAnalysisLogQCNoSerializer(qcno, many=True)
        return Response(serializer.data)

# --------------------- Data Analysis ------------------------


# Raw Materials

# class RMMaterialsListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMMaterialsListReportingSerializer
#
#
# class RMBatchNoListReportingView(generics.ListAPIView):
#     queryset = RMAnalysisItems.objects.all()
#     serializer_class = RMBatchNoListReportingSerializer


class ProductDataAnalysisView(generics.ListAPIView):
    queryset = ProductAnalysisItemsLog.objects.all()
    serializer_class = ProductAnalysisItemsReportingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['ProductAnalysisID__QCNo__batchNo__ProductCode__Product',
                        'ProductAnalysisID__QCNo__batchNo__batchNo',
                        'ProductAnalysisID__QCNo__QCNo',
                        'parameter',
                        'ProductAnalysisID__QCNo__sampleStage'
                        ]
    # -------------- ANALYST LOGIN -------------


#   Pending RM Samples

class ProductCurrentAnalystSampleView(APIView):
    def get(self, request):
        user = request.user
        if user.role == 'QC_Analyst':
            samples = ProductSamples.objects.filter(analyst=user.id, status="ASSIGNED")
            dict = []
            for i in samples:
                dic = {}
                name = i.batchNo.ProductCode.Product
                dic['QCNo'] = i.QCNo
                dic['Product'] = name
                dic['stage'] = i.sampleStage
                dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y")
                dict.append(dic)
            return Response(dict)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
