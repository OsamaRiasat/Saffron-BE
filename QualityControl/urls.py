from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# router.register('Products', ProductViews, basename='Products')


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),
    # path('populateRMParameters/', PopulateParametersView.as_view()),

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
    path('RMspecifications/', RMSpecificationsView.as_view()),
    path('RMAcquirespecifications/<str:RMCode>/', RMAcquireSpecificationsView.as_view()),
    path('AcquireRMCode/', AcquireRMCodeListView.as_view()),
    path('Acquirermaterial/', AcquireRMaterialListView.as_view()),

    # RM Edit Specs
    # path('AcquireRMCode/', AcquireRMCodeListView.as_view()),
    # path('Acquirermaterial/', AcquireRMaterialListView.as_view()),
    path('RMEditSpecifications/<str:RMCode>/', RMEditSpecsView.as_view()),
    path('TempRMSpecifications/', TEMPRMSpecificationsView.as_view()),

    # RM Sample Assignment
    path('RMSamples/', RMSamplesView.as_view()),
    path('UnBlockedAnalysts/', AnalystView.as_view()),
    path('AssignAnalyst/<str:pk>/', AssignAnalystView.as_view()),


    #Reporting
    path('specificationReporting', specificationReportingView.as_view()),
    path('RMQCNoList/', RMQCNoView.as_view()),
    # RM Data Entry
    path('RMQCNoSample/<str:QCNo>/', RMQCNoSampleView.as_view()),
    path('PostRMAnalysis/', PostRMAnalysisView.as_view()),

    #---------------Block Analyst---------------------#

    path('BlockUnBlockAnalyst/<int:id>', BlockUnBlockAnalystView.as_view()),
    path('AllAnalyst/', AllAnalystView.as_view()),

    #------------ COA Approval --------------#
    path('RMAnalysisQCNo/', RMAnalysisQCNoView.as_view()),
    path('RMAnalysis/<str:QCNo>/', RMAnalysisView.as_view()),
    path('RejectAnalysis/<str:QCNo>/', RejectRMAnalysisView.as_view()),
    path('ReleaseRMAnalysis/<str:QCNo>/', ReleaseRMAnalysisView.as_view()),

]