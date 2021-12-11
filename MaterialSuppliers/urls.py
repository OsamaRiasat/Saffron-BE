from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# Suppliers

urlpatterns = [
    path('suppliers', suppliers.as_view()),

    #   Add Supplier

    path('AddSupplier', AddSupplierView.as_view()),

    #   Approve Materials
    path('ShowSuppliers', ShowSuppliersView.as_view()),
    path('AddMaterialToSuppliersView', AddMaterialToSuppliersView.as_view()),

]
