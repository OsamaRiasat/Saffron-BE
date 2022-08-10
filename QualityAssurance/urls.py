from django.urls import path

from QualityControl.views import AllStageByPCodeView
from .views import *
from Production.views import PCodesForLineClearanceView

urlpatterns = [
    #   -----------------       RM SAMPLE     ---------------
    path('GRNOList/', GRNOListView.as_view()),
    path('RawMaterialListFromSpecifications/', RawMaterialListFromSpecificationsView().as_view()),
    path('SuppliersList', SuppliersListView.as_view()),
    path('GetQcNo/', GetQcNoView.as_view()),
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
    path('Raw_Material_Auto_Code_Generator<str:Type>', Raw_Material_Auto_Code_Generator_View.as_view()),
    path('AddRawMaterial/', RawMaterialView.as_view()),

    #   ---------------     View RM    ----------------------

    path('RawMaterialDetail/', RawMaterialDetailView.as_view()),

    # -------------- Add Packing Material ----------------

    path('Packing_Material_Auto_Code_Generator<str:Type>', Packing_Material_Auto_Code_Generator_View.as_view()),
    path('AddPackingMaterial/', PackingMaterialView.as_view()),


    #   ---------------     View PM    ----------------------

    path('PackingMaterialDetail/', PackingMaterialDetailView.as_view()),
    # QualityAssurance/PackingMaterialDetail/?PMCode=&Material=&Units=&Type=

    # -------------- Batch Deviation ----------------

    path('HighestBDNo/', HighestBDNoView.as_view()),
    # path('ProductCode/', PCodesForLineClearanceView.as_view()),
    path('ProductNameByProductCode/<str:ProductCode>/', ProductNameByProductCodeView.as_view()),
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
    path('ChangeControlNumbersList/', ChangeControlNumbersListView.as_view()),
    path('ChangeControlGetData/<str:pk>', ChangeControlGetDataView.as_view()),
    path('changeControlVerificationOfChanges/<str:pk>', changeControlVerificationOfChangesView.as_view()),
    path('QAs', QAsView.as_view()),

    # -------------------- Dispensation Request DRF -----------------------
    # /inventory/viewset/RawMaterialNames/
    # /inventory/viewset/RawMaterialCodes/
    # /inventory/RawMaterialSearchByName/{Material}/
    # /inventory/RawMaterialSearchByRMCode/{RMCode}/
    path('HighestDRFNo/', HighestDRFNoView.as_view()),
    path('DRFPostView/', DRFPostView.as_view()),

    # -------------------- Product Sample -----------------------
    path('PSPCode/', PSPCodeView.as_view()),   # Product Code List
    path('PSBatchNo/<str:Pcode>/', PSBatchNoView.as_view()),    # When Product COde is selected
    path('PSBatchDetail/<str:batchNo>/', PSBatchDetailView.as_view()),  # When batch No is selected
    path('stagesList/<str:ProductCode>',AllStageByPCodeView.as_view()),
    # path('AllUsers/', AllUsersView.as_view()), # Sampled by list
    path('ProductSample/', ProductSampleView.as_view()), # Post api


    # -------------- Batch Review ----------------
    path('BRPCode/', BRPCodeView.as_view()),
    path('BRBatchNo/<str:Pcode>/', BRBatchNoView.as_view()),
    path('BRBatchDetail/<str:batchNo>/', BRBatchDetailView.as_view()),
    path('BRDetail/', BRDetailView.as_view()),

]
