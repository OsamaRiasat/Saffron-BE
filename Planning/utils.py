
from .models import ProductMaterials,PlanItems
from Products.models import Formulation
from django.db.models import Min

def convertUnitsToPacks(units, PackSize,dosageForm):
    if dosageForm=="Tablet" or dosageForm=="Capsule":
        l = PackSize.split('x')
        num1 = int(l[0])
        num2 = int(l[1])
        size = num1*num2
        # Size per Pack
        return units/size
    elif dosageForm =="Vial":
        size = int(PackSize)
        # Size per Pack
        return size

def convertPacksToUnits(Packs, PackSize,dosageForm):
    if dosageForm=="Tablet" or dosageForm=="Capsule":
        l = PackSize.split('x')
        num1 = int(l[0])
        num2 = int(l[1])
        size = num1*num2
        # Total Number of Units
        return Packs*size
    elif dosageForm =="Vial":
        size = int(PackSize)
        # Size per Pack
        return size

def MergeMaterials(planNo):
    data = ProductMaterials.objects.filter(planNo=planNo)
    resp = {}
    for obj in data:
        if obj.RMCode.RMCode in resp:
            resp[obj.RMCode.RMCode]["ReqQty"]=resp[obj.RMCode.RMCode]["ReqQty"] + obj.requiredQuantity
            resp[obj.RMCode.RMCode]["demandedQuantity"] = resp[obj.RMCode.RMCode]["demandedQuantity"] + obj.demandedQuantity
        else:
            resp[obj.RMCode.RMCode]={}
            resp[obj.RMCode.RMCode]["ReqQty"]= obj.requiredQuantity
            resp[obj.RMCode.RMCode]["Inhand"] = obj.inHandQuantity
            resp[obj.RMCode.RMCode]["demandedQuantity"] = obj.demandedQuantity
            resp[obj.RMCode.RMCode]["RMCode"] = obj.RMCode.RMCode
            resp[obj.RMCode.RMCode]["Material"] = obj.RMCode.Material
            resp[obj.RMCode.RMCode]["Units"] = obj.RMCode.Units

    return resp

def ProductionCalculationUtil(planNo):
    data = PlanItems.objects.filter(planNo=planNo)
    l=[]
    for obj in data:
        query = ProductMaterials.objects.filter(planNo=planNo, ProductCode=obj.ProductCode)
        minWB = query.all().aggregate(Min('workableBatches'))["workableBatches__min"]
        stdbatchsize = Formulation.objects.filter(ProductCode=obj.ProductCode).first().batchSize
        if minWB>0:
            dic={}
            stdbatchsize= Formulation.objects.filter(ProductCode=obj.ProductCode).first().batchSize
            requiredQty = stdbatchsize * obj.noOfBatchesToBePlanned
            packsRequired = convertUnitsToPacks(requiredQty, obj.PackSize, obj.ProductCode.dosageForm.dosageForm)
            workableUnits = minWB * stdbatchsize
            workablePacks = convertUnitsToPacks(workableUnits,obj.PackSize, obj.ProductCode.dosageForm.dosageForm)

            dic["Rank of Plan"]= "First Line"
            dic["Product"] = obj.ProductCode.Product
            dic["PacSize"] = obj.PackSize
            dic["BatchesToBePlanned"] = obj.noOfBatchesToBePlanned
            dic["WorkableBatches"] = minWB
            dic["packsRequired"]=packsRequired
            dic["workablePacks"] = workablePacks
            l.append(dic)


        else:
            dic = {}
            stdbatchsize = Formulation.objects.filter(ProductCode=obj.ProductCode).first().batchSize
            requiredQty = stdbatchsize * obj.noOfBatchesToBePlanned
            packsRequired = convertUnitsToPacks(requiredQty, obj.PackSize, obj.ProductCode.dosageForm.dosageForm)
            workableUnits = minWB * stdbatchsize
            workablePacks = convertUnitsToPacks(workableUnits,obj.PackSize, obj.ProductCode.dosageForm.dosageForm)
            dic["Rank of Plan"] = "Second Line"
            dic["Product"] = obj.ProductCode.Product
            dic["PacSize"] = obj.PackSize
            dic["BatchesToBePlanned"] = obj.noOfBatchesToBePlanned
            dic["WorkableBatches"] = minWB
            dic["packsRequired"] = packsRequired
            dic["workablePacks"] = workablePacks
            l.append(dic)

        #print(minWB)
    return l