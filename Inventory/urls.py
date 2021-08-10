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

    # RMDemands
    path('RMDemands/', RMDemandsView.as_view()),
    path('RMDemandHighestDNo/', RMDemandHighestDNoView.as_view()),
    path('RMDemandsDNosWithPendingStatus/', RMDemandsDNosWithPendingStatus.as_view()),

    # RMPurchase Orders
    path('RMPurchaseOrderHighestPONo/', RMPurchaseOrderHighestPONoView.as_view()),
    path('RMPurchaseOrderListOfMaterialsForForm/<str:SID>/<int:DNo>',
         RMPurchaseOrderListOfMaterialsForFormView.as_view()),
    path('RMPurchaseOrder/', RMPurchaseOrdersViews.as_view()),


    # RM Receiving

    # IGP
    path('RMPurchaseOrderPONOsWithPendingStatus/', RMDemandsDNosWithPendingStatus.as_view()),
    path('RMPurchaseOrderItemsCodesForReceiving/<str:PONo>/', RMPurchaseOrderItemsCodesForReceivingView.as_view()),
    path('RMPurchaseOrderDetails/<str:PONo>/<str:RMCode>/', RMPurchaseOrderDetailsView.as_view()),
    path('RMHighestIGPNO', RMHighestIGPNO.as_view()),
    path('RMIGP', RMIGPView.as_view()),

    # GRN
    path('IGPNo/',IGPNoView),
]
