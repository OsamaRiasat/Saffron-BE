from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

urlpatterns = [

    # path('populateRMParameters/', PopulateParametersView.as_view()),
    # path('populatePMParameters/', PopulatePMParametersView.as_view()),
    path('populateProductParameters/', PopulateProductParametersView.as_view()),

    # -----------------------------------------------------------------------------------------
    # -----------------------------     RAW MATERIALS     -----------------------------------

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
    # path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),


    #         --------------    PENDING REPORTS    -----------

    path('Print_RMAnalysisQCNo/', Print_RMAnalysisQCNoView.as_view()),
    path('Print_RMAnalysis/<str:QCNo>/', Print_RMAnalysisView.as_view()),
    path('RMAnalysisLogPrint/<str:qc>/', RMAnalysisLogPrintView.as_view()),
    # path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

    #         --------------    Label Printing    -----------

    path('Label_Print_RMAnalysisQCNo/', Label_Print_RMAnalysisQCNoView.as_view()),
    # path('Print_ProductAnalysis/<str:QCNo>/', Print_RMAnalysisView.as_view()),

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

    # -----------------------------------------------------------------------------------------
    # -----------------------------     PACKING MATERIALS     -----------------------------------

    #           -------------   SPECIFICATIONS  -----------

    # RM View Specs
    path('PMCodeListOfSpecifications/', PMCodeListOfSpecificationsView.as_view()),
    path('PMMaterialListOfSpecifications/', PMMaterialListOfSpecificationsView.as_view()),
    path('PMViewSpecifications/<str:PMCode>/', PMViewSpecificationsView.as_view()),
    path('PMNameByPMCodeForViewSpecs/<str:PMCode>/', PMNameByPMCodeForViewSpecsView.as_view()),
    path('PMCodeByPMNameForViewSpecs/<str:PMName>/', PMCodeByNameForViewSpecsView.as_view()),

    # RM New Specs
    path('PMCodeList/', PMCodeView.as_view()),
    path('PMCodeByPMName/<str:name>/', PMCodeByNameView.as_view()),
    path('PMaterialList/', PMaterialView.as_view()),
    path('PMNameByPMCode/<str:PMCode>/', PMNameByPMCodeView.as_view()),
    # path('RMReference/', RMReferenceView.as_view()),
    path('PMParameters/', PMParametersView.as_view()),
    path('PMspecifications/', PMSpecificationsView.as_view()),  # Post Specifications
    path('AcquirePMCode/', AcquirePMCodeListView.as_view()),
    path('PMAcquirermaterial/', AcquirePMaterialListView.as_view()),
    path('PMAcquirespecifications/<str:PMCode>/', PMAcquireSpecificationsView.as_view()),

    # RM Edit Specs
    # path('AcquireRMCode/', AcquireRMCodeListView.as_view()),
    # path('Acquirermaterial/', AcquireRMaterialListView.as_view()),
    # path('RMNameByRMCodeForViewSpecs/<str:RMCode>/', RMNameByRMCodeForViewSpecsView.as_view()),
    # path('RMCodeByRMNameForViewSpecs/<str:RMName>/', RMCodeByNameForViewSpecsView.as_view()),
    path('PMEditSpecifications/<str:PMCode>/', PMEditSpecsView.as_view()),
    path('TempPMSpecifications/', TEMPPMSpecificationsView.as_view()),

    #         --------------    SAMPLE ASSIGNMENT   -----------

    # PM Sample Assignment
    path('PMSamples/', PMSamplesView.as_view()),
    # path('Analysts/', AnalystView.as_view()),
    path('PMAnalystSample/<int:id>/', PMAnalystSampleView.as_view()),
    path('PMAssignAnalyst/<str:pk>/', PMAssignAnalystView.as_view()),

    #         --------------    DATA ENTRY     -----------

    # PM Data Entry
    path('PMQCNo/', PMQCNoView.as_view()),
    path('PMQCNoSample/<str:QCNo>/', PMQCNoSampleView.as_view()),
    path('PostPMAnalysis/', PostPMAnalysisView.as_view()),

    #         --------------    COA APPROVAL    -----------

    # PM COA Approval
    path('PMAnalysisQCNo/', PMAnalysisQCNoView.as_view()),
    path('PMAnalysis/<str:QCNo>/', PMAnalysisView.as_view()),
    path('PostPMCOAApproval/<str:QCNo>/', PostPMCOAApprovalView.as_view()),
    # path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

    #         --------------    PENDING REPORTS    -----------

    path('Print_PMAnalysisQCNo/', Print_PMAnalysisQCNoView.as_view()),
    path('Print_PMAnalysis/<str:QCNo>/', Print_PMAnalysisView.as_view()),
    path('PMAnalysisLogPrint/<str:qc>/', PMAnalysisLogPrintView.as_view()),

    #         --------------    Label Printing    -----------

    path('Label_Print_PMAnalysisQCNo/', Label_Print_PMAnalysisQCNoView.as_view()),
    # path('Print_PMAnalysis/<str:QCNo>/', Print_PMAnalysisView.as_view()),


    #         --------------    REPORTING   -----------

    # RM Reporting
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    path('PMDataAnalysis', PMDataAnalysisView.as_view()),
    # /QualityControl/RMDataAnalysis?RMAnalysisID__QCNo__IGPNo__RMCode__Material=&RMAnalysisID__QCNo__IGPNo__batchNo=&RMAnalysisID__QCNo__QCNo=&parameter=

    #       ----------------    Analyst Login   ------------

    path('PMCurrentAnalystSample/', PMCurrentAnalystSampleView.as_view()),

    # -----------------------------------------------------------------------------------------
    # -----------------------------     PRODUCTS     -----------------------------------

    # Product View Specs
    path('ProductCodeListOfSpecifications/', ProductCodeListOfSpecificationsView.as_view()),
    path('ProductListOfSpecifications/', ProductListOfSpecificationsView.as_view()),
    path('ProductStageListOfSpecifications/<str:ProductCode>/', ProductStageListOfSpecificationsView.as_view()),
    path('ProductViewSpecifications/<str:ProductCode>/<str:stage>/', ProductViewSpecificationsView.as_view()),
    path('ProductNameByProductCodeForViewSpecs/<str:ProductCode>/', ProductNameByProductCodeForViewSpecsView.as_view()),
    path('ProductCodeByProductNameForViewSpecs/<str:Product>/', ProductCodeByNameForViewSpecsView.as_view()),

    # Product New Specs
    path('ProductCodeList/', ProductCodeView.as_view()),
    path('ProductCodeByProductName/<str:name>/', ProductCodeByNameView.as_view()),
    path('ProductList/', ProductView.as_view()),
    path('ProductNameByProductCode/<str:ProductCode>/', ProductNameByProductCodeView.as_view()),
    path('newStagelist/<str:ProductCode>', StageByPCodeView.as_view()),
    # path('RMReference/', RMReferenceView.as_view()),
    path('ProductParameters/', ProductParametersView.as_view()),
    path('Productspecifications/', ProductSpecificationsView.as_view()),  # Post Specifications
    path('AcquireProductCode/', AcquireProductCodeListView.as_view()),
    path('ProductAcquirermaterial/', AcquireProductListView.as_view()),
    path('ProductStageListOfSpecifications/<str:ProductCode>/', ProductStageListOfSpecificationsView.as_view()),

    path('ProductAcquirespecifications/<str:ProductCode>/<str:stage>/', ProductAcquireSpecificationsView.as_view()),

    # Product Edit Specs
    # path('AcquireProductCode/', AcquireRMCodeListView.as_view()),
    # path('AcquireProduct/', AcquireRMaterialListView.as_view()),
    # path('ProductStageListOfSpecifications/<str:ProductCode>',ProductStageListOfSpecificationsView.as_view()),
    # path('ProductNameByProductCodeForViewSpecs/<str:RMCode>/', RMNameByRMCodeForViewSpecsView.as_view()),
    # path('ProductCodeByProductNameForViewSpecs/<str:RMName>/', RMCodeByNameForViewSpecsView.as_view()),
    path('allStagelist/<str:ProductCode>', AllStageByPCodeView.as_view()),
    path('ProductEditSpecifications/<str:ProductCode>/<str:stage>/', ProductEditSpecsView.as_view()),
    path('TempProductSpecifications/', TEMPProductSpecificationsView.as_view()),

    #         --------------    SAMPLE ASSIGNMENT   -----------

    # Product Sample Assignment
    path('ProductSamples/', ProductSamplesView.as_view()),
    # path('Analysts/', AnalystView.as_view()),
    path('ProductAnalystSample/<int:id>/', ProductAnalystSampleView.as_view()),
    path('ProductAssignAnalyst/<str:pk>/', ProductAssignAnalystView.as_view()),

    #         --------------    DATA ENTRY     -----------

    # Product Data Entry
    path('ProductQCNo/', ProductQCNoView.as_view()),
    path('ProductQCNoSample/<str:QCNo>/', ProductQCNoSampleView.as_view()),
    path('PostProductAnalysis/', PostProductAnalysisView.as_view()),

    #         --------------    COA APPROVAL    -----------

    # Product COA Approval
    path('ProductAnalysisQCNo/', ProductAnalysisQCNoView.as_view()),
    path('ProductAnalysis/<str:QCNo>/', ProductAnalysisView.as_view()),
    path('PostProductCOAApproval/<str:QCNo>/', PostProductCOAApprovalView.as_view()),
    # path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

    #         --------------    PENDING REPORTS    -----------

    path('Print_ProductAnalysisQCNo/', Print_ProductAnalysisQCNoView.as_view()),
    path('Print_ProductAnalysis/<str:QCNo>/', Print_ProductAnalysisView.as_view()),
    path('ProductAnalysisLogPrint/<str:qc>/', ProductAnalysisLogPrintView.as_view()),

    #         --------------    Label Printing    -----------

    path('Label_Print_ProductAnalysisQCNo/', Label_Print_ProductAnalysisQCNoView.as_view()),
    # path('Print_ProductAnalysis/<str:QCNo>/', Print_ProductAnalysisView.as_view()),

    #         --------------    REPORTING   -----------

    # RM Reporting
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    # path('RMMaterialsListReporting/', RMMaterialsListReportingView.as_view()),
    path('ProductDataAnalysis', ProductDataAnalysisView.as_view()),
    # /QualityControl/RMDataAnalysis?RMAnalysisID__QCNo__IGPNo__RMCode__Material=&RMAnalysisID__QCNo__IGPNo__batchNo=&RMAnalysisID__QCNo__QCNo=&parameter=

    #       ----------------    Analyst Login   ------------

    path('ProductCurrentAnalystSample/', ProductCurrentAnalystSampleView.as_view()),
]
