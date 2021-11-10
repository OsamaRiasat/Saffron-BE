from django.db.models import Max
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Products.models import PackSizes,Formulation
from .utils import *

# A-Product Selection

class highestPlanNoView(APIView):
    def get(self, request):
        planNo = Plan.objects.all().aggregate(Max('planNo'))
        return Response(planNo)

# class ProductNamesViews(viewsets.ModelViewSet):
#     serializer_class = ProductNamesSerializer
#     queryset = Products.objects.all()

class ProductNamesViews(APIView):
    def get(self,request):
        data = PackSizes.objects.all()
        l = []
        for obj in data:
            dic = {}
            dic["Product"]=obj.ProductCode.Product
            l.append(dic)
        return Response(l)

class ProductCodesViews(APIView):
    def get(self,request):
        data = PackSizes.objects.all()
        l = []
        for obj in data:
            dic = {}
            dic["ProductCode"]=obj.ProductCode.ProductCode
            l.append(dic)
        return Response(l)

#
# class ProductCodesViews(viewsets.ModelViewSet):
#     serializer_class = ProductCodesSerializer
#     queryset = Products.objects.all()
#

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
            FGS_Packs = 20000  # No of Packs from Goods Stock
            WIP_Units = 40000  # No of Units From Production
            WIP_Packs = convertUnitsToPacks(WIP_Units,PackSize,dosageForm)
        elif isFGS=="True":
            FGS_Packs = 20000  # No of Packs From Goods Stock
        elif isWIP=="True":
            WIP_Units = 40000  # No of Units From Production
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
                         "batchesToBePlanned":round(batchesToBePlanned,3)})


# B-Material Calculation

class  PlanMaterialCalculationView(APIView):
    def get(self,request, planNo, isQuarantine, isPIP):
        data = PlanItems.objects.filter(planNo=planNo).exclude(noOfBatchesToBePlanned=0)
        tempBinCards={}
        for obj in data:
            formulation  = Formulation.objects.filter(ProductCode=obj.ProductCode)
            for i in formulation:
                requiredQuantity = obj.noOfBatchesToBePlanned*i.quantity
                inHandQty = 0
                if i.RMCode in tempBinCards:
                    inHandQty = tempBinCards[i.RMCode]
                else:
                    inHandQty = 200 # Value from BinCard
                inHandQty2 = inHandQty
                demandedQty = requiredQuantity - inHandQty
                if demandedQty<0:
                    demandedQty=0
                inHandQty = inHandQty-demandedQty
                if inHandQty<0:
                    inHandQty=0
                tempBinCards[i.RMCode]= inHandQty
                plan = Plan.objects.get(planNo=planNo)
                noOfBatchesToBePlanned = PlanItems.objects.get(planNo=planNo,ProductCode=obj.ProductCode,PackSize=obj.PackSize).noOfBatchesToBePlanned
                workableBatches = (noOfBatchesToBePlanned/requiredQuantity)*inHandQty2
                planItemMaterial = ProductMaterials.objects.create(planNo= plan,
                                                                   ProductCode=obj.ProductCode,
                                                                   PackSize=obj.PackSize,
                                                                   RMCode=i.RMCode,
                                                                   requiredQuantity=requiredQuantity,
                                                                   demandedQuantity=demandedQty,
                                                                   inHandQuantity=inHandQty2,
                                                                   workableBatches=round(workableBatches,1))
                planItemMaterial.save()

        resp = MergeMaterials(planNo)
        l=[]
        for item in resp:
            l.append(resp[item])
        return  Response({"list":l})


class BackToProductSelectionView(APIView):

    def get(self, request, planNo):
        data = PlanItems.objects.only('ProductCode', 'PackSize', 'inHandPacks', 'packsToBePlanned', 'noOfBatchesToBePlanned','requiredPacks').filter(planNo=planNo)
        l = []

        for obj in data:
            dic = {}
            dic["Product"] = obj.ProductCode.Product
            dic["ProductCode"]=obj.ProductCode.ProductCode
            dic["PackSize"] = obj.PackSize
            dic["inHandPacks"] = obj.inHandPacks
            dic["packsToBePlanned"] = obj.packsToBePlanned
            dic["noOfBatchesToBePlanned"] = obj.noOfBatchesToBePlanned
            dic["requiredPacks"]=obj.requiredPacks
            l.append(dic)

        # plan = Plan.objects.get(planNo=planNo)
        # plan.delete()

        return Response(l)

# C-Production Calculation

class ProductionCalculationView(APIView):
    def get(self,request, planNo):

        resp = ProductionCalculationUtil(planNo)
        return Response({"list":resp})


class PostPlanView(generics.CreateAPIView):
    serializer_class = PostPlanSerializer
    queryset = Plan.objects.all()