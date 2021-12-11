from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# router.register('Products', ProductViews, basename='Products')


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),

    # ----------------- Batch Issuance Request  -----------

    path('PlanNo/', PlanNoView.as_view()),
    path('ProductByPlanNo/<int:planNo>/', ProductByPlanNoView.as_view()),
    path('SBS/<str:PCode>/', SBSView.as_view()),
    path('BatchIssuenceRequest/', BatchIssuenceRequestView.as_view()),

    # ------------------ Issue Batch No --------------

    path('PlanNoBIR/', PlanNoBIRView.as_view()),
    path('PCodeBIR/<int:planNo>/', PCodeBIRView.as_view()),
    path('IssueBatchNo/', IssueBatchNoView.as_view()),
    path('Formulation/', FormulationView.as_view()),
    path('BPRLog/', BPRLogView.as_view()),

    # -----------------   Batch Track    --------------

    path('PCodeBPR/', PCodeBPRView.as_view()),  # list of Pcodes
    path('BPRByPcodeView/<str:PCode>/', BPRByPcodeView.as_view()),  # List of Batch no
    path('GeneralDataBPRLog/', GeneralDataBPRLogView.as_view()),
    path('DataFromBPR/<str:PCode>/', DataFromBPRView.as_view()),
    path('BatchStages/', BatchStagesView.as_view()),

    # -----------------    Daily Packing      --------------
    # path('PlanNo/', PlanNoView.as_view()),
    # path('ProductByPlanNo/<int:planNo>/', ProductByPlanNoView.as_view()),
    path('WhenProductIsSelected/<str:PCode>/', WhenProductIsSelectedView.as_view()),
    path('PackingLog/', PackingLogView.as_view()),

    # -----------------    Line Clearance      --------------

    path('PCodesForLineClearance/', PCodesForLineClearanceView.as_view()),
    path('BatchNoBYPCode/<str:PCode>/', BatchNoBYPCodeView.as_view()),
    path('WhenBatchNoIsSelected/<str:batchNo>/', WhenBatchNoIsSelectedView.as_view()),

    # ----------------      Close Order      --------------------

    path('PlanItems/', PlanItemsView.as_view()),
    path('PlanStatus/', PlanStatusView.as_view()),

    #   ----------------     Raw Material Assessment    -------------------

    path('ListOfPCodeForAssessment/', ListOfPCodeForAssessmentView.as_view()),
    path('ListOfPNameForAssessment/', ListOfPNameForAssessmentView.as_view()),
    path('PCodeByPNameAssessment/<str:PName>/', PCodeByPNameAssessmentView.as_view()),
    path('PackSizesList/<str:PCode>/',PackSizesListView.as_view()),
    path('ViewFormulationForAssessment/<str:Pcode>/<int:batch_size>/<str:noOfBatches>/', ViewFormulationForAssessmentView.as_view()),

    #   ----------------     Packing Material Assessment    -------------------

    path('ListOfPCodeForPMAssessment/', ListOfPCodeForPMAssessmentView.as_view()),
    path('ListOfPNameForPMAssessment/', ListOfPNameForPMAssessmentView.as_view()),
    #path('PCodeByPNameAssessment/<str:PName>/', PCodeByPNameAssessmentView.as_view()),
    # path('PackSizesList/<str:PCode>/', PackSizesListView.as_view()),
    path('ViewFormulationForPMAssessment/<str:Pcode>/<int:batch_size>/<str:noOfBatches>/<str:packSize>/',
         ViewFormulationForPMAssessmentView.as_view()),

    # --------------------New Formulation -----------------------

    path('PCodeList/', PCodeView.as_view()),
    path('PNameList/', PNameView.as_view()),
    path('PCodeByPname/<path:Product>/', PCodeByPnameView.as_view()),
    path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    path('PackSizeList/<str:PCode>/', PackSizesView.as_view()),
    path('PMCodeList/', PMCodeView.as_view()),
    path('PMNameList/', PMNameView.as_view()),
    path('PMCodeByName/<str:PMName>/', PMCodeByNameView.as_view()),
    path('PMNameByPMCode/<str:PMCode>/', PMNameByPMCodeView.as_view()),
    path('PMData/<str:PMCode>/', PMDataView.as_view()),
    path('AddPMFormulation/', PMFormulationsView.as_view()),

    # --------------------Edit Formulation -----------------------

    path('FPCodeList/', FPCodeView.as_view()),
    path('FPNameList/', FPNameView.as_view()),
    # path('PCodeByPname/<str:Product>/', PCodeByPnameView.as_view()),
    # path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    path('ProductPMFormulation/<str:Pcode>/<str:PackSize>/', ProductPMFormulationView.as_view()),
    # path('PMCodeList/', PMCodeView.as_view()),
    # path('PMNameList/', PMNameView.as_view()),
    # path('PMCodeByName/<str:PMName>/', PMCodeByNameView.as_view()),
    # path('PMNameByPMCode/<str:PMCode>/', PMNameByPMCodeView.as_view()),
    # path('PMData/<str:PMCode>/', PMDataView.as_view()),

]
