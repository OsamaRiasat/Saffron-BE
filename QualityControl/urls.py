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
    path('RMEditSpecifications/<str:RMCode>/', RMEditSpecsView.as_view()),
    path('TempRMSpecifications/', TEMPRMSpecificationsView.as_view()),

    #         --------------    SAMPLE ASSIGNMENT   -----------

    # RM Sample Assignment
    path('RMSamples/', RMSamplesView.as_view()),
    path('Analysts/', AnalystView.as_view()),
    path('AssignAnalyst/<str:pk>/', AssignAnalystView.as_view()),

    #         --------------    DATA ENTRY     -----------

    # RM Data Entry
    path('RMQCNoSample/<str:QCNo>/', RMQCNoSampleView.as_view()),
    path('PostRMAnalysis/', PostRMAnalysisView.as_view()),

    #         --------------    COA APPROVAL    -----------

    # RM COA Approval
    path('RMAnalysisQCNo/', RMAnalysisQCNoView.as_view()),
    path('RMAnalysis/<str:QCNo>/', RMAnalysisView.as_view()),
    path('RejectAnalysis/<str:QCNo>/', RejectRMAnalysisView.as_view()),
    path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

    #         --------------    REPORTING   -----------

    # RM Reporting
    path('RMDataAnalysis', RMDataAnalysisView.as_view()),
    # /QualityControl/RMDataAnalysis?RMAnalysisID__QCNo__IGPNo__RMCode__Material=New%20Coat%20Brown&RMAnalysisID__QCNo__IGPNo__batchNo=ok-12-12&RMAnalysisID__QCNo__QCNo=RM23232&parameter=Taste

    #         --------------    ANALYST MANAGEMENT  -----------

    # Analyst Management
    path('BlockUnBlockAnalyst/<int:id>', BlockUnBlockAnalystView.as_view()),
    path('AllAnalyst/', AllAnalystView.as_view()),

]
