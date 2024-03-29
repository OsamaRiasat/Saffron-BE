from django.db.models import Max
from rest_framework import viewsets, generics, status

from Production.models import PMFormulation
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from Products.models import PackSizes, Formulation
from .utils import *


# A-Product Selection

class highestPlanNoView(APIView):
    def get(self, request):
        planNo = Plan.objects.all().aggregate(Max('planNo'))
        return Response(planNo)


class ProductNamesViews(APIView):
    def get(self, request):
        pcode = Formulation.objects.all()

        l1 = []
        for i in pcode:
            l1.append(i.ProductCode.Product)


        packsizes = PackSizes.objects.all()
        l2 = []
        for i in packsizes:
            l2.append(i.ProductCode.Product)

        intersection = set.intersection(set(l1), set(l2))
        l = []
        for PCode in intersection:
            dic = {}
            dic["Product"] = PCode
            l.append(dic)
        return Response(l)


class ProductCodesViews(APIView):
    def get(self, request):
        pcode = Formulation.objects.all()

        l1 = []
        for i in pcode:
            l1.append(i.ProductCode.ProductCode)

        packsizes = PackSizes.objects.only('ProductCode').all()
        l2 = []
        for i in packsizes:
            l2.append(i.ProductCode.ProductCode)
        intersection = set.intersection(set(l1), set(l2))
        l = []
        for PCode in intersection:
            dic = {}
            dic["ProductCode"] = PCode
            l.append(dic)
        return Response(l)


class ProductDetailsByCodeView(APIView):  # When the Product Code is Selected (also change for name)

    def get(self, request, ProductCode):
        Product = Products.objects.get(ProductCode=ProductCode).Product
        dosage = Products.objects.get(ProductCode=ProductCode).dosageForm.dosageForm
        PackSizesList = []
        Query = PackSizes.objects.filter(ProductCode=ProductCode)
        print(Query)
        for obj in Query:
            PackSizesList.append(obj.PackSize)

        batchSize = Formulation.objects.filter(ProductCode=ProductCode).first().batchSize
        return Response({"PackSizesList": PackSizesList,
                         "Product": Product,
                         "dosageType": dosage,
                         "units": batchSize,
                         "batches": 1})


class ProductDetailsByNameView(APIView):

    def get(self, request, Product):
        ProductCode = Products.objects.get(Product=Product).ProductCode
        dosage = Products.objects.get(ProductCode=ProductCode).dosageForm.dosageForm
        PackSizesList = []
        Query = PackSizes.objects.filter(ProductCode=ProductCode)
        for obj in Query:
            PackSizesList.append(obj.PackSize)

        batchSize = Formulation.objects.filter(ProductCode=ProductCode).first().batchSize
        return Response({"PackSizesList": PackSizesList,
                         "ProductCode": ProductCode,
                         "units": batchSize,
                         "dosageType": dosage,
                         "batches": 1})


class GoodsStockDetailsView(APIView):
    def get(self, request, ProductCode, PackSize, Packs, isFGS, isWIP):
        FGS_Packs = 0
        WIP_Packs = 0
        batchesToBePlanned = 0
        dosageForm = Products.objects.get(ProductCode=ProductCode).dosageForm.dosageForm

        if isFGS == "True" and isWIP == "True":
            FGS_Packs = 20000  # No of Packs from Goods Stock
            WIP_Units = 40000  # No of Units From Production
            WIP_Packs = convertUnitsToPacks(WIP_Units, PackSize, dosageForm)
        elif isFGS == "True":
            FGS_Packs = 20000  # No of Packs From Goods Stock
        elif isWIP == "True":
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
            batchesToBePlanned = unitsToBePlanned / stdBatchSize

        return Response({"FGS_Packs": FGS_Packs,
                         "WIP_Packs": WIP_Packs,
                         "Inhand_Packs": Inhand_Packs,
                         "packsToBePlanned": packsToBePlanned,
                         "batchesToBePlanned": round(batchesToBePlanned, 3)})


class PostPlanView(generics.CreateAPIView):
    serializer_class = PostPlanSerializer
    queryset = Plan.objects.all()


class Update_Plan_And_PlanItems_View(generics.UpdateAPIView):
    queryset = Plan.objects.all()
    serializer_class = UpdatePlanSerializer


# B-Material Calculation

class PlanMaterialCalculationView(APIView):
    def get(self, request, planNo, isQuarantine, isPIP):
        data = PlanItems.objects.filter(planNo=planNo).exclude(noOfBatchesToBePlanned=0)
        tempBinCards = {}
        for obj in data:
            formulation = Formulation.objects.filter(ProductCode=obj.ProductCode)
            for i in formulation:
                requiredQuantity = obj.noOfBatchesToBePlanned * i.quantity
                inHandQty = 0
                if i.RMCode in tempBinCards:
                    inHandQty = tempBinCards[i.RMCode]
                else:
                    inHandQty = 200  # Value from BinCard
                inHandQty2 = inHandQty
                demandedQty = requiredQuantity - inHandQty
                if demandedQty < 0:
                    demandedQty = 0
                inHandQty = inHandQty - demandedQty
                if inHandQty < 0:
                    inHandQty = 0
                tempBinCards[i.RMCode] = inHandQty
                plan = Plan.objects.get(planNo=planNo)
                noOfBatchesToBePlanned = PlanItems.objects.get(planNo=planNo, ProductCode=obj.ProductCode,
                                                               PackSize=obj.PackSize).noOfBatchesToBePlanned
                workableBatches = (noOfBatchesToBePlanned / requiredQuantity) * inHandQty2
                planItemMaterial = ProductMaterials.objects.create(planNo=plan,
                                                                   ProductCode=obj.ProductCode,
                                                                   PackSize=obj.PackSize,
                                                                   RMCode=i.RMCode,
                                                                   requiredQuantity=requiredQuantity,
                                                                   demandedQuantity=demandedQty,
                                                                   inHandQuantity=inHandQty2,
                                                                   workableBatches=round(workableBatches, 1))
                planItemMaterial.save()

        resp = MergeMaterials(planNo)
        l = []
        for item in resp:
            l.append(resp[item])
        return Response({"list": l})


class BackToProductSelectionView(APIView):

    def get(self, request, planNo):
        data = PlanItems.objects.only('ProductCode', 'PackSize', 'inHandPacks', 'packsToBePlanned',
                                      'noOfBatchesToBePlanned', 'requiredPacks').filter(planNo=planNo)
        l = []

        for obj in data:
            dic = {}
            dic["Product"] = obj.ProductCode.Product
            dic["ProductCode"] = obj.ProductCode.ProductCode
            dic["PackSize"] = obj.PackSize
            dic["inHandPacks"] = obj.inHandPacks
            dic["packsToBePlanned"] = obj.packsToBePlanned
            dic["noOfBatchesToBePlanned"] = obj.noOfBatchesToBePlanned
            dic["requiredPacks"] = obj.requiredPacks
            l.append(dic)

        # plan = Plan.objects.get(planNo=planNo)
        # plan.delete()

        return Response(l)


# C-Production Calculation

class ProductionCalculationView(APIView):
    def get(self, request, planNo):
        resp = ProductionCalculationUtil(planNo)
        return Response({"list": resp})


class DeletePlanView(generics.DestroyAPIView):
    queryset = Plan.objects.all()
    #
    # def destroy(self, request, *args, **kwargs):
    #     # Do logic here to get `course_participant` to delete, then
    #     self.delete(request=request)
    #
    #     # Don't return super().destroy(request, *args, **kwargs)
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class save_plan_View(APIView):
    def get(self, request, planNo):
        try:
            obj = Plan.objects.get(planNo=planNo)
            obj.isSaved = True
            obj.save()
            message = "Plan Saved"
            return Response({"message": message}, status=status.HTTP_200_OK)
        except Exception as e:
            message = "Plan Couldn't be saved"
            print(e)
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)

    #   ------------- Packing Material Planning     -----------


# class PlanNosListView(generics.ListAPIView):
#     queryset = Plan.objects.all()
#     serializer_class = planNumbersSerializer

class PlanPackingMaterialCalculationView(APIView):
    def get(self, request, planNo, isQuarantine, isPIP):
        data = PlanItems.objects.filter(planNo=planNo).exclude(noOfBatchesToBePlanned=0)
        tempBinCards = {}
        ifAlreadyCalculated = ProductPackingMaterials.objects.filter(planNo=planNo)
        lis = []
        for obj in ifAlreadyCalculated:
            dic = {}
            dic["ReqQty"]= obj.requiredQuantity
            dic["Inhand"] = obj.inHandQuantity
            dic["demandedQuantity"] = obj.demandedQuantity
            dic["RMCode"] = obj.PMCode.PMCode
            dic["Material"] = obj.PMCode.Material
            dic["Units"] = obj.PMCode.Units
            lis.append(dic)

        if len(lis):
            return Response({"list":lis})

        for obj in data:
            formulation = PMFormulation.objects.filter(ProductCode=obj.ProductCode, PackSize=obj.   PackSize)
            for i in formulation:
                requiredQuantity = obj.noOfBatchesToBePlanned * i.quantity
                inHandQty = 0
                if i.PMCode in tempBinCards:
                    inHandQty = tempBinCards[i.RMCode]
                else:
                    inHandQty = 200  # Value from BinCard
                inHandQty2 = inHandQty
                demandedQty = requiredQuantity - inHandQty
                if demandedQty < 0:
                    demandedQty = 0
                inHandQty = inHandQty - demandedQty
                if inHandQty < 0:
                    inHandQty = 0
                tempBinCards[i.PMCode] = inHandQty
                plan = Plan.objects.get(planNo=planNo)
                noOfBatchesToBePlanned = PlanItems.objects.get(planNo=planNo, ProductCode=obj.ProductCode,
                                                               PackSize=obj.PackSize).noOfBatchesToBePlanned
                workableBatches = (noOfBatchesToBePlanned / requiredQuantity) * inHandQty2
                planItemMaterial = ProductPackingMaterials.objects.create(planNo=plan,
                                                                   ProductCode=obj.ProductCode,
                                                                   PackSize=obj.PackSize,
                                                                   PMCode=i.PMCode,
                                                                   requiredQuantity=requiredQuantity,
                                                                   demandedQuantity=demandedQty,
                                                                   inHandQuantity=inHandQty2,
                                                                   workableBatches=round(workableBatches, 1))
                planItemMaterial.save()

        resp = MergePackingMaterials(planNo)
        l = []
        for item in resp:
            l.append(resp[item])
        return Response({"list": l})
