from rest_framework.routers import DefaultRouter
from django.urls import path, include

from Inventory.views import PlanNosListView
from .views import *

router = DefaultRouter()
# A-Product Selection Form
# router.register('ProductNames', ProductNamesViews, basename='ProductNames')
# router.register('ProductCodes', ProductCodesViews, basename='ProductNames')

urlpatterns = [

    # A-Product Selection
    path('viewset/ProductCodes/', ProductCodesViews.as_view()),
    path('viewset/ProductNames/', ProductNamesViews.as_view()),
    path('highestPlanNo/', highestPlanNoView.as_view()),
    path('ProductDetailsByCode/<str:ProductCode>/', ProductDetailsByCodeView.as_view()),
    path('ProductDetailsByName/<str:Product>/', ProductDetailsByNameView.as_view()),
    path('GoodsStockDetails/<str:ProductCode>/<str:PackSize>/<int:Packs>/<str:isFGS>/<str:isWIP>/',
         GoodsStockDetailsView.as_view()),
    path('PostPlan/', PostPlanView.as_view()),
    path('Update_Plan_And_PlanItems/<int:pk>/', Update_Plan_And_PlanItems_View.as_view()),
    # B-Material Packing
    path('PlanMaterialCalculation/<int:planNo>/<str:isQuarantine>/<str:isPIP>/', PlanMaterialCalculationView.as_view()),
    path('BackToProductSelection/<int:planNo>/', BackToProductSelectionView.as_view()),

    # C-Production
    path('ProductionCalculation/<int:planNo>', ProductionCalculationView.as_view()),

    path('DeletePlan/<int:pk>', DeletePlanView.as_view()),
    path('save_plan/<int:planNo>', save_plan_View.as_view()),


    # Packing Material Planning

    path('PlanNo_List_for_Planning', PlanNosListView.as_view()),
    # path('BackToProductSelection/<int:planNo>/', BackToProductSelectionView.as_view()),
    path('PlanPackingMaterialCalculation/<int:planNo>/<str:isQuarantine>/<str:isPIP>/', PlanPackingMaterialCalculationView.as_view()),




]
