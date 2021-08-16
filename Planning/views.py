
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Products.models import PackSizes,Formulation
from .utils import *
# A-Product Selection

class ProductNamesViews(viewsets.ModelViewSet):
    serializer_class = ProductNamesSerializer
    queryset = Products.objects.all()


class ProductCodesViews(viewsets.ModelViewSet):
    serializer_class = ProductCodesSerializer
    queryset = Products.objects.all()


class ProductDetailsByCodeView(APIView):

    def get(self, request, ProductCode):
        Product = Products.objects.get(ProductCode=ProductCode).Product

        PackSizesList = []
        Query = PackSizes.objects.filter(ProductCode=ProductCode)
        for obj in Query:
            PackSizesList.append(obj.PackSize)

        batchSize = Formulation.objects.filter(ProductCode=ProductCode).first().batchSize
        return Response({"PackSizesList": PackSizesList,
                         "Product": Product,
                         "units": batchSize,
                         "batches": 1})


class ProductDetailsByNameView(APIView):

    def get(self,request,Product):
        ProductCode = Products.objects.get(Product=Product).ProductCode
        PackSizesList = []
        Query = PackSizes.objects.filter(ProductCode=ProductCode)
        for obj in Query:
            PackSizesList.append(obj.PackSize)

        batchSize = Formulation.objects.filter(ProductCode=ProductCode).first().batchSize
        return Response({"PackSizesList":PackSizesList,
                         "ProductCode":ProductCode,
                         "units":batchSize,
                         "batches":1})

class GoodsStockDetailsView(APIView):
    def get(self,request, ProductCode, PackSize, Packs ,isFGS, isWIP):
        FGS_Packs=0
        WIP_Packs=0
        batchesToBePlanned=0
        dosageForm = Products.objects.get(ProductCode=ProductCode).dosageForm.dosageForm

        if isFGS=="True" and isWIP=="True":
            FGS_Packs = 2000  # No of Packs from Goods Stock
            WIP_Units = 20000  # No of Units From Production
            WIP_Packs = convertUnitsToPacks(WIP_Units,PackSize,dosageForm)
        elif isFGS=="True":
            FGS_Packs = 2000  # No of Packs From Goods Stock
        elif isWIP=="True":
            WIP_Units = 20000  # No of Units From Production
            WIP_Packs = convertUnitsToPacks(WIP_Units, PackSize, dosageForm)


        Inhand_Packs = FGS_Packs + WIP_Packs

        if Inhand_Packs > Packs:
            packsToBePlanned = 0
        else:
            packsToBePlanned = Packs - Inhand_Packs

        if packsToBePlanned > 0:
            unitsToBePlanned = convertPacksToUnits(packsToBePlanned, PackSize, dosageForm)
            stdBatchSize = Formulation.objects.filter(ProductCode=ProductCode).first().batchSize
            batchesToBePlanned = unitsToBePlanned/stdBatchSize

        return Response({"FGS_Packs":FGS_Packs,
                         "WIP_Packs":WIP_Packs,
                         "Inhand_Packs":Inhand_Packs,
                         "packsToBePlanned":packsToBePlanned,
                         "batchesToBePlanned":batchesToBePlanned})

# class RMDemandedItemsView(viewsets.ModelViewSet):
#     serializer_class = RMDemandItemsSerializer
#     queryset = RMDemandedItems.objects.all()

class PostPlanView(generics.CreateAPIView):
    serializer_class = PostPlanSerializer
    queryset = Plan.objects.all()