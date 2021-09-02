from django.urls import path
from .views import *


urlpatterns = [
    path('GRNOList/',GRNOListView.as_view()),
    path('RMRecievingDetailByGRNo/<int:GRNo>/',RMReceivingDetailsByGRNoView.as_view()),
    path('RMSample/',RMSampleView.as_view()),
]