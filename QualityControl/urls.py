from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

urlpatterns = [

    # path('populateRMParameters/', PopulateParametersView.as_view()),

    #           -------------   SPECIFICATIONS  -----------

    # RM View Specs
    path('RMCodeListOfSpecifications/', RMCodeListOfSpecificationsView.as_view()),
    path('RMMaterialListOfSpecifications/', RMMaterialListOfSpecificationsView.as_view()),
    path('RMViewSpecifications/<str:RMCode>/', RMViewSpecificationsView.as_view()),
    path('RMNameByRMCodeForViewSpecs/<str:RMCode>/', RMNameByRMCodeForViewSpecsView.as_view()),
    path('RMCodeByRMNameForViewSpecs/<str:RMName>/', RMCodeByNameForViewSpecsView.as_view()),

    # RM New Specs
    path('RMCodeList/', RMCodeView.as_view()),
    path('RMCodeByRMName/<str:name>/', RMCodeByNameView.as_view()),
    path('RMaterialList/', RMaterialView.as_view()),
    path('RMNameByRMCode/<str:RMCode>/', RMNameByRMCodeView.as_view()),
    path('RMReference/', RMReferenceView.as_view()),
    path('RMParameters/', RMParametersView.as_view()),
    path('RMspecifications/', RMSpecificationsView.as_view()),  # Post Specifications
    path('AcquireRMCode/', AcquireRMCodeListView.as_view()),
    path('Acquirermaterial/', AcquireRMaterialListView.as_view()),
    path('RMAcquirespecifications/<str:RMCode>/', RMAcquireSpecificationsView.as_view()),

    # RM Edit Specs
    # path('AcquireRMCode/', AcquireRMCodeListView.as_view()),
    # path('Acquirermaterial/', AcquireRMaterialListView.as_view()),
    # path('RMNameByRMCodeForViewSpecs/<str:RMCode>/', RMNameByRMCodeForViewSpecsView.as_view()),
    # path('RMCodeByRMNameForViewSpecs/<str:RMName>/', RMCodeByNameForViewSpecsView.as_view()),
    path('RMEditSpecifications/<str:RMCode>/', RMEditSpecsView.as_view()),
    path('TempRMSpecifications/', TEMPRMSpecificationsView.as_view()),

    #         --------------    SAMPLE ASSIGNMENT   -----------

    # RM Sample Assignment
    path('RMSamples/', RMSamplesView.as_view()),
    path('Analysts/', AnalystView.as_view()),
    path('AnalystSample/<int:id>/', AnalystSampleView.as_view()),
    path('AssignAnalyst/<str:pk>/', AssignAnalystView.as_view()),

    #         --------------    DATA ENTRY     -----------

    # RM Data Entry
    path('RMQCNo/', RMQCNoView.as_view()),
    path('RMQCNoSample/<str:QCNo>/', RMQCNoSampleView.as_view()),
    path('PostRMAnalysis/', PostRMAnalysisView.as_view()),

    #         --------------    COA APPROVAL    -----------

    # RM COA Approval
    path('RMAnalysisQCNo/', RMAnalysisQCNoView.as_view()),
    path('RMAnalysis/<str:QCNo>/', RMAnalysisView.as_view()),
    path('PostRMCOAApproval/<str:QCNo>/', PostRMCOAApprovalView.as_view()),
    #path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

    #         --------------    REPORTING   -----------

    # RM Reporting
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    path('RMDataAnalysis', RMDataAnalysisView.as_view()),
    # /QualityControl/RMDataAnalysis?RMAnalysisID__QCNo__IGPNo__RMCode__Material=&RMAnalysisID__QCNo__IGPNo__batchNo=&RMAnalysisID__QCNo__QCNo=&parameter=

    #       ----------------    Analyst Login   ------------

    path('CurrentAnalystSample/', CurrentAnalystSampleView.as_view()),


    #         --------------    ANALYST MANAGEMENT  -----------

    # Analyst Management
    path('BlockUnBlockAnalyst/<int:id>', BlockUnBlockAnalystView.as_view()),
    path('AllAnalyst/', AllAnalystView.as_view()),

]
