from django.urls import path
from .views import *


urlpatterns = [
    #   -----------------       RM SAMPLE     ---------------
    path('GRNOList/', GRNOListView.as_view()),
    path('RMRecievingDetailByGRNo/<int:GRNo>/', RMReceivingDetailsByGRNoView.as_view()),
    path('RMSample/', RMSampleView.as_view()),

    #   -----------------       PM SAMPLE     ---------------

    path('PMGRNOList/',PMGRNOListView.as_view()),
    path('PMRecievingDetailByGRNo/<int:GRNo>/',PMReceivingDetailsByGRNoView.as_view()),
    path('PMSample/',PMSampleView.as_view()),


]