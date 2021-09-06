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

    # populate DB

    path('PopulateCategory/', PopulateCategoryView.as_view()),

    # -----------------     NCR     ---------------

    path('AllUsers/', AllUsersView.as_view()),
    path('CategoriesList/', CategoriesView.as_view()),
    path('SubCategories/<str:category>/', SubCategoriesView.as_view()),
    path('ProductCode/', PCodesForLineClearanceView.as_view()),
    path('BatchNo/<str:Pcode>/', BatchNoView.as_view()),
    path('HighestNCR/', HighestNCRView.as_view()),
    path('NCR/', NCRView.as_view()),

    # ------------      Print NCR     -----------------

    path('NCRNoList/', NCRNoView.as_view()),
    path('NCRDetail/<int:NCRNo>/', NCRDetailView.as_view()),

    # ----------------     Close NCR    -------------------

    path('NCRNoStatusOpenList/', NCRNoStatusOpenView.as_view()),
    # path('NCRDetail/<int:NCRNo>/', NCRDetailView.as_view()),
    path('CloseNCR/<int:pk>/', CloseNCRView.as_view()),

    # ----------------     Close Batch    -------------------

    path('OpenBatches/', OpenBatchesView.as_view()),
    path('CloseBPR/<str:pk>/', CloseBPRView.as_view()),

    # ----------------   Add Product   -----------------

    path('ListOfDosageForms/', ListOfDosageForms.as_view()),
    path('AddProduct/', AddProductView.as_view()),

    # ----------------   View Product   -----------------

    # path('AllProductCode/', ProductCodeView.as_view()),
    path('ProductDetail/', ProductDetailView.as_view()),
    # http://127.0.0.1:8000/QualityAssurance/ProductDetail/?ProductCode__Product=&ProductCode=&ProductCode__RegistrationNo=&ProductCode__ShelfLife=

    # -------------- Add Raw Material ----------------#
    path('AddRawMaterial/', RawMaterialView.as_view()),

    #   ---------------     View RM    ----------------------

    path('RawMaterialDetail/', RawMaterialDetailView.as_view()),

    # -------------- Add Packing Material ----------------

    path('AddPackingMaterial/', PackingMaterialView.as_view()),
    # QualityAssurance/PackingMaterialDetail/?PMCode=&Material=&Units=&Type=

    #   ---------------     View PM    ----------------------

    path('PackingMaterialDetail/', PackingMaterialDetailView.as_view()),

    # -------------- Batch Deviation ----------------

    path('HighestBDNo/', HighestBDNoView.as_view()),
    # path('ProductCode/', PCodesForLineClearanceView.as_view()),
    # path('BatchNo/<str:Pcode>/', BatchNoView.as_view()),
    path('BatchDetail/<str:batchNo>/', BatchDetailView.as_view()),
    path('BatchDeviation/', BatchDeviationView.as_view()),

    # -------------- Batch Deviation ----------------#
    path('AllBDNo/', AllBDNoView.as_view()),
    path('BatchDeviationDetail/<int:pk>/', BatchDeviationDetailView.as_view()),

    # ------------------ Change Control ---------------------#
    path('HighestCCNo/', HighestCCNoView.as_view()),
    # path('ProductCode/', PCodesForLineClearanceView.as_view()),
    # path('BatchNo/<str:Pcode>/', BatchNoView.as_view()),s
    path('ChangeControl/', ChangeControlView.as_view()),

]
