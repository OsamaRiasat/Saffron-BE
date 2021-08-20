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

]
