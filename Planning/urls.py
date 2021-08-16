from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *


router = DefaultRouter()
# A-Product Selection Form
router.register('ProductNames', ProductNamesViews, basename='ProductNames')
router.register('ProductCodes', ProductCodesViews, basename='ProductNames')

urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),

# A-Product Selection
    path('ProductDetailsByCode/<str:ProductCode>/', ProductDetailsByCodeView.as_view()),
    path('ProductDetailsByName/<str:Product>/', ProductDetailsByNameView.as_view()),
    path('GoodsStockDetails/<str:ProductCode>/<str:PackSize>/<int:Packs>/<str:isFGS>/<str:isWIP>/',GoodsStockDetailsView.as_view()),
    path('PostPlan/',PostPlanView.as_view()),

    # path('PMRecievingDetailByGRNo/<int:GRNo>/', PMReceivingDetailsByGRNoView.as_view()),
    # path('PMGRNoList/', PMGRNoView.as_view(), name='GRNo'),
    # path('PMBinCard/', PMBinCardView.as_view()),

]
