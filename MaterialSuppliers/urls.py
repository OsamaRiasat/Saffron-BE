from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# Suppliers
router.register('Suppliers', SuppliersViews, basename='Suppliers')
router.register('SupplierApprovedItems', SupplierApprovedItemsViews, basename='SupplierApprovedItems')
router.register('SupplierIDS', SupplierIDsViews, basename='SuppliersIDS')



urlpatterns = [
    path('viewset/', include(router.urls)),
    path('SupplierApprovedMaterials/<int:pk>/', SupplierApprovedMaterialsView.as_view()),

]
