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
    path('RMFormulation/', FormulationsView.as_view()),
    #Populate Product Table
    path('PopulateProductTable/',PopulateProductView.as_view()),
    path('PopulateFormulationTable/',PopulateRMFormulationView.as_view()),

    # --------------------New Formulation -----------------------#
    path('PCodeList/', PCodeView.as_view()),
    path('PNameList/', PNameView.as_view()),
    path('PCodeByPname/<str:Product>/', PCodeByPnameView.as_view()),
    path('PnameByPCode/<str:Pcode>/', PnameByPCodeView.as_view()),
    path('RMCodeList/', RMCodeView.as_view()),
    path('RMNameList/', RMNameView.as_view()),
    path('RMCodeByName/<str:RMName>/', RMCodeByNameView.as_view()),
    path('RMNameByRMCode/<str:RMCode>/', RMNameByRMCodeView.as_view()),
    path('RMData/<str:RMCode>/', RMDataView.as_view()),

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
]
