from django.urls import path
from .views import *
from Production.views import PCodesForLineClearanceView

urlpatterns = [
    #   -----------------       RM SAMPLE     ---------------
    path('GRNOList/', GRNOListView.as_view()),
    path('RMRecievingDetailByGRNo/<int:GRNo>/', RMReceivingDetailsByGRNoView.as_view()),
    path('RMSample/', RMSampleView.as_view()),

    #   -----------------       PM SAMPLE     ---------------

    path('PMGRNOList/', PMGRNOListView.as_view()),
    path('PMRecievingDetailByGRNo/<int:GRNo>/', PMReceivingDetailsByGRNoView.as_view()),
    path('PMSample/', PMSampleView.as_view()),
    #populate DB
    path('PopulateCategory/',PopulateCategoryView.as_view()),
    #----------------- NCR ---------------#
    path('AllUsers/', AllUsersView.as_view()),
    path('CategoriesList/', CategoriesView.as_view()),
    path('SubCategories/<str:category>/', SubCategoriesView.as_view()),
    path('ProductCode/', PCodesForLineClearanceView.as_view()),
    path('BatchNo/<str:Pcode>/',BatchNoView.as_view()),
    path('HighestNCR/', HighestNCRView.as_view()),
    path('NCR/', NCRView.as_view()),
    #------------ Print NCR -----------------#
    path('NCRNoList/', NCRNoView.as_view()),
    path('NCRDetail/<int:NCRNo>/', NCRDetailView.as_view()),
    #---------------- Close NCR -------------------#
    path('NCRNoStatusOpenList/', NCRNoStatusOpenView.as_view()),
    # path('NCRDetail/<int:NCRNo>/', NCRDetailView.as_view()),
    path('CloseNCR/<int:pk>/',CloseNCRView.as_view()),


]