from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# Products
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
]
