from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# router.register('Products', ProductViews, basename='Products')
# router.register('DosageForms', DosageFormsViews, basename='DosageForms')
# router.register('PackSizes', PackSizesViews, basename='PackSizes')


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),

    # RM Formulation

    # Populate Product Table
    path('PopulateProductTable/', PopulateProductView.as_view()),
    path('PopulateFormulationTable/', PopulateRMFormulationView.as_view()),

    # --------------------New Formulation -----------------------#

    path('PCodeList/', PCodeView.as_view()),
    path('PNameList/', PNameView.as_view()),
    path('PCodeByPname/<path:Product>/', PCodeByPnameView.as_view()),
    path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    path('RMCodeList/', RMCodeView.as_view()),
    path('RMNameList/', RMNameView.as_view()),
    path('RMCodeByName/<str:RMName>/', RMCodeByNameView.as_view()),
    path('RMNameByRMCode/<str:RMCode>/', RMNameByRMCodeView.as_view()),
    path('RMData/<str:RMCode>/', RMDataView.as_view()),
    path('RMFormulation/', FormulationsView.as_view()),

    # --------------------New PM Formulation (newer)-----------------------#

    path('PCode_For_PM_Formulation', PCode_For_PM_Formulation_View.as_view()),
    path('PName_For_PM_Formulation', PName_For_PM_Formulation_View.as_view()),
    # path('PCodeByPname/<path:Product>/', PCodeByPnameView.as_view()),
    # path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    # /Production/PackSizeList/{PCode}/
    path('batchsize/<str:Pcode>', batchsize_View.as_view()),
    path('PMCodeList', PMCodeView.as_view()),
    path('PMNameList', PMNameView.as_view()),
    path('PMCodeByName/<str:PMName>', PMCodeByNameView.as_view()),
    path('PMNameByPMCode/<str:PMCode>', PMNameByPMCodeView.as_view()),
    path('PMData/<str:PMCode>', PMDataView.as_view()),
    path('PM_Formulation/', PM_FormulationsView.as_view()),

    # --------------------Edit Formulation -----------------------#
    path('FPCodeList/', FPCodeView.as_view()),
    path('FPNameList/', FPNameView.as_view()),
    # path('PCodeByPname/<str:Product>/', PCodeByPnameView.as_view()),
    # path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    path('ProductFormulation/<str:Pcode>/', ProductFormulationView.as_view()),
    # path('RMCodeList/', RMCodeView.as_view()),
    # path('RMNameList/', RMNameView.as_view()),
    # path('RMCodeByName/<str:RMName>/', RMCodeByNameView.as_view()),
    # path('RMNameByRMCode/<str:RMCode>/', RMNameByRMCodeView.as_view()),
    # path('RMData/<str:RMCode>/', RMDataView.as_view()),

    # ---------------- Add PackSize -----------------------

    path('ProductCodeListForPackSize/', ProductCodeListForPackSizeView.as_view()),
    path('ProductData/<str:pk>/', ProductDataView.as_view()),
    path('AddPackSize/', AddPackSizeView.as_view()),

]
