import re
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from .models import *
from Inventory.models import RawMaterials
from .serializers import *
from Account.models import User
from django_filters.rest_framework import DjangoFilterBackend, filters


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


# --------------------- SPECIFICATIONS ------------------------

# A. Raw Materials

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
        rmcode = RawMaterials.objects.all()
        serializer = RMCodeSerializer(rmcode, many=True)
        return Response(serializer.data)


class RMCodeByNameView(APIView):
    def get(self, request, name):

        rmcode = RawMaterials.objects.get(Material=name)
        check = RMSpecifications.objects.filter(RMCode=rmcode.RMCode)
        if check:
            return Response({'message': 'Material have already specifications'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = RMCodeSerializer(rmcode)
            return Response(serializer.data)


class RMaterialView(APIView):
    def get(self, request):
        rm = RawMaterials.objects.all()
        serializer = RMaterialSerializer(rm, many=True)
        return Response(serializer.data)


class RMNameByRMCodeView(APIView):
    def get(self, request, RMCode):
        check = RMSpecifications.objects.filter(RMCode=RMCode)
        if check:
            return Response({'message': 'Material have already specifications'}, status=status.HTTP_400_BAD_REQUEST)
        else:
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
            name = i.IGPNo.RMCode.Material
            dic['QCNo'] = i.QCNo
            dic['Material'] = name
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
            rm_receiving = RMReceiving.objects.get(IGPNo=i.IGPNo.IGPNo)
            rm = RawMaterials.objects.get(RMCode=rm_receiving.RMCode.RMCode)
            dic['Date'] = i.samplingDateTime.strftime("%d.%m.%Y %H:%M")
            dic['Material'] = rm.Material
            dic['Unit'] = rm.Units
            dic['Quantity'] = rm_receiving.quantityReceived
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

        rm_receiving = RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)

        dict = {}
        dict['samplingDateTime'] = sample.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = sample.IGPNo.IGPNo
        dict['assignedDateTime'] = sample.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = sample.analyst.username

        dict['RMCode'] = rm_receiving.RMCode.RMCode
        dict['Material'] = rm_receiving.RMCode.Material
        dict['Units'] = rm_receiving.RMCode.Units
        dict['quantityReceived'] = rm_receiving.quantityReceived
        dict['batchNo'] = rm_receiving.batchNo
        dict['MFG_Date'] = rm_receiving.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = rm_receiving.EXP_Date.strftime("%d.%m.%Y")

        data = {}
        spec = RMSpecifications.objects.get(RMCode=rm_receiving.RMCode.RMCode)
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
        rm_receiving = RMReceiving.objects.get(IGPNo=samples.IGPNo.IGPNo)
        dict = {}
        dict['samplingDateTime'] = samples.samplingDateTime.strftime("%d.%m.%Y %H:%M")
        dict['QCNo'] = QCNo
        dict['IGPNo'] = rm_receiving.IGPNo
        dict['RMCode'] = rm_receiving.RMCode.RMCode
        dict['Material'] = rm_receiving.RMCode.Material
        dict['Units'] = rm_receiving.RMCode.Units
        dict['quantityReceived'] = rm_receiving.quantityReceived
        dict['batchNo'] = rm_receiving.batchNo
        dict['MFG_Date'] = rm_receiving.MFG_Date.strftime("%d.%m.%Y")
        dict['EXP_Date'] = rm_receiving.EXP_Date.strftime("%d.%m.%Y")
        dict['quantityApproved'] = analysis.quantityApproved
        dict['quantityRejected'] = analysis.quantityRejected
        dict['rawDataReference'] = analysis.rawDataReference
        dict['workingStd'] = analysis.workingStd
        dict['analysisDateTime'] = analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M")
        dict['retestDate'] = analysis.retestDate.strftime("%d.%m.%Y %H:%M")
        dict['assignedDateTime'] = samples.assignedDateTime.strftime("%d.%m.%Y %H:%M")
        dict['analyst'] = samples.analyst.username
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
        result = data.get('result', None)

        if result == "Reject":
            analysis = RMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = RMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=analysis,
                analysisDateTime=analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M"),
                retestDate=analysis.retestDate.strftime("%d.%m.%Y"),
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
            return Response({"message": "Rejected"})
        else:
            sample = RMSamples.objects.get(QCNo=QCNo)
            analysis = RMAnalysis.objects.get(QCNo=QCNo)
            log_analysis = RMAnalysisLog.objects.create(
                workingStd=analysis.workingStd,
                rawDataReference=analysis.rawDataReference,
                QCNo=sample,
                analysisDateTime=analysis.analysisDateTime.strftime("%d.%m.%Y %H:%M"),
                retestDate=analysis.retestDate.strftime("%d.%m.%Y"),
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
            rm = RMReceiving.objects.get(IGPNo=sample.IGPNo.IGPNo)
            rm.quantityApproved = analysis.quantityApproved
            rm.quantityRejected = analysis.quantityRejected
            rm.save()
            sample.status = "APPROVED"
            sample.result = "Released"
            sample.save()
            analysis.delete()
            return Response({"message": "Released"})


# class ReleaseRMAnalysisView(APIView):
#     serializer_class = RemarksSerializer
#
#     def post(self, request, QCNo):
#         data = request.data
#         remarks = data.get('remarks', None)


# --------------------- Data Analysis ------------------------


# Raw Materials

class RMMaterialsListReportingView(generics.ListAPIView):
    queryset = RMAnalysisItems.objects.all()
    serializer_class = RMMaterialsListReportingSerializer


class RMBatchNoListReportingView(generics.ListAPIView):
    queryset = RMAnalysisItems.objects.all()
    serializer_class = RMBatchNoListReportingSerializer


class RMDataAnalysisView(generics.ListAPIView):
    queryset = RMAnalysisItems.objects.all()
    serializer_class = RMAnalysisItemsReportingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['RMAnalysisID__QCNo__IGPNo__RMCode__Material',
                        'RMAnalysisID__QCNo__IGPNo__batchNo',
                        'RMAnalysisID__QCNo__QCNo',
                        'parameter',
                        'RMAnalysisID__QCNo__IGPNo__S_ID__S_Name']
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
            samples = RMSamples.objects.filter(analyst=user.id)
            dict = []
            for i in samples:
                dic = {}
                name = i.IGPNo.RMCode.Material
                dic['QCNo'] = i.QCNo
                dic['Material'] = name
                dic['assignedDateTime'] = i.assignedDateTime.strftime("%d.%m.%Y")
                dict.append(dic)
            return Response(dict)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
