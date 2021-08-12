from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


router = DefaultRouter()

# Raw Materials
router.register('RawMaterialTypes', RawMaterialTypesViews, basename='RawMaterialTypes')
router.register('RawMaterials', RawMaterialsViews, basename='RawMaterials')
router.register('RawMaterialCodes', RawMaterialCodesViews, basename='RawMaterialCodes')
router.register('RawMaterialNames', RawMaterialNamesViews, basename='RawMaterialName')

# Packing Materials
router.register('PackingMaterialTypes', PackingMaterialTypesViews, basename='PackingMaterialTypes')
router.register('PackingMaterials', PackingMaterialsViews, basename='PackingMaterials')
router.register('PackingMaterialCodes', PackingMaterialCodesViews, basename='PackingMaterialCodes')
router.register('PackingMaterialNames', PackingMaterialNamesViews, basename='PackingMaterialName')

# Demands

# router.register('RMDemands', RMDemandsView, basename='RMDemands')
# router.register('RMDemandedItems', RMDemandedItemsView, basename='RMDemandedItems')

# RM Purchase Orders

# router.register('RMPurchaseOrderItems', RMPurchaseOrdersItemsView, basename='RMPurchaseOrderItems')

# RM Receiving
# router.register('RMIGP', RMIGPView, basename='RMIGP')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),

    # Raw Materials
    path('RawMaterialSearchByName/<str:Material>/', RawMaterialSearchByName.as_view()),
    path('RawMaterialSearchByRMCode/<str:RMCode>/', RawMaterialSearchByRMCode.as_view()),

    # Packing Materials
    path('PackingMaterialSearchByName/<str:Material>/', PackingMaterialSearchByName.as_view()),
    path('PackingMaterialSearchByPMCode/<str:PMCode>/', PackingMaterialSearchByPMCode.as_view()),

    # RMDemands
    path('RMDemands/', RMDemandsView.as_view()),
    path('RMDemandHighestDNo/', RMDemandHighestDNoView.as_view()),
    path('RMDemandsDNosWithPendingStatus/', RMDemandsDNosWithPendingStatus.as_view()),

    # PMDemands
    path('PMDemands/', PMDemandsView.as_view()),
    path('PMDemandHighestDNo/', PMDemandHighestDNoView.as_view()),
    path('PMDemandsDNosWithPendingStatus/', PMDemandsDNosWithPendingStatus.as_view()),

    # RMPurchase Orders
    path('RMPurchaseOrderHighestPONo/', RMPurchaseOrderHighestPONoView.as_view()),
    path('RMPurchaseOrderListOfMaterialsForForm/<str:SID>/<int:DNo>',
         RMPurchaseOrderListOfMaterialsForFormView.as_view()),
    path('RMPurchaseOrder/', RMPurchaseOrdersViews.as_view()),

    # PMPurchase Orders
    path('PMPurchaseOrderHighestPONo/', PMPurchaseOrderHighestPONoView.as_view()),
    path('PMPurchaseOrderListOfMaterialsForForm/<str:SID>/<int:DNo>',
         PMPurchaseOrderListOfMaterialsForFormView.as_view()),
    path('PMPurchaseOrder/', PMPurchaseOrdersViews.as_view()),



    # RM Receiving

    # IGP
    path('RMPurchaseOrderPONOsWithPendingStatus/', RMPurchaseOrdersWithOpenStatusView.as_view()),
    path('RMPurchaseOrderItemsCodesForReceiving/<str:PONo>/', RMPurchaseOrderItemsCodesForReceivingView.as_view()),
    path('RMPurchaseOrderDetails/<str:PONo>/<str:RMCode>/', RMPurchaseOrderDetailsView.as_view()),
    path('RMHighestIGPNO', RMHighestIGPNO.as_view()),
    path('RMIGP', RMIGPView.as_view()),


    #Generate GRN
    path('IGPNoList/',IGPNoView.as_view(),name='IGPNo'),
    path('HighestGRNo/',RMHighestGRNO.as_view()),
    path('RMRecievingDetail/<int:IGPNo>/',RMReceivingDetailsView.as_view()),
    path('UpdateRMRecieving/<int:pk>/',UpdateRMReceivingDetailsView.as_view()),
    #POST GRN
    path('RMRecievingDetailByGRNo/<int:GRNo>/',RMReceivingDetailsByGRNoView.as_view()),
    path('GRNoList/',GRNoView.as_view(),name='GRNo'),
    path('RMBinCard/',RMBinCardView.as_view()),

    # PM Receiving

    # IGP
    path('PMPurchaseOrderPONOsWithPendingStatus/', PMPurchaseOrdersWithOpenStatusView.as_view()),
    path('PMPurchaseOrderItemsCodesForReceiving/<str:PONo>/', PMPurchaseOrderItemsCodesForReceivingView.as_view()),
    path('PMPurchaseOrderDetails/<str:PONo>/<str:PMCode>/', PMPurchaseOrderDetailsView.as_view()),
    path('PMHighestIGPNO', PMHighestIGPNO.as_view()),
    path('PMIGP', PMIGPView.as_view()),

    # Generate GRN
    path('PMIGPNoList/', PMIGPNoView.as_view(), name='PMIGPNo'),
    path('PMHighestGRNo/', PMHighestGRNO.as_view()),
    path('PMRecievingDetail/<int:IGPNo>/', PMReceivingDetailsView.as_view()),
    path('UpdatePMRecieving/<int:pk>/', UpdatePMReceivingDetailsView.as_view()),
    # POST GRN
    path('PMRecievingDetailByGRNo/<int:GRNo>/', PMReceivingDetailsByGRNoView.as_view()),
    path('PMGRNoList/', PMGRNoView.as_view(), name='GRNo'),
    path('PMBinCard/', PMBinCardView.as_view()),

]
