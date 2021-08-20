from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()



# router.register('Products', ProductViews, basename='Products')



urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<str:pk>/', include(router.urls)),

    # RM Specs
    path('populateRMParameters/', PopulateParametersView.as_view()),
    path('RMCodeList/', RMCodeView.as_view()),
    path('RMCodeByRMName/<str:name>/', RMCodeByNameView.as_view()),
    path('RMaterialList/', RMaterialView.as_view()),
    path('RMNameByRMCode/<str:id>/', RMNameByRMCodeView.as_view()),
    path('reference/', RMReferenceView.as_view()),
    path('parameters/', RMParametersView.as_view()),
    path('rmspecifications/', RMSpecificationsView.as_view()),
    path('acquirespecifications/<str:id>/', AcquireSpecificationsView.as_view()),
    path('acquireRMCode/', AcquireRMCodeListView.as_view()),
    path('acquirermaterial/', AcquireRMaterialListView.as_view()),
]
