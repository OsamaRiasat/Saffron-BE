
from .models import ProductMaterials


def convertUnitsToPacks(units, PackSize,dosageForm):
    if dosageForm=="Tablet" or dosageForm=="Capsule":
        l = PackSize.split('x')
        num1 = int(l[0])
        num2 = int(l[1])
        size = num1*num2
        # Size per Pack
        return units/size

def convertPacksToUnits(Packs, PackSize,dosageForm):
    if dosageForm=="Tablet":
        l = PackSize.split('x')
        num1 = int(l[0])
        num2 = int(l[1])
        size = num1*num2
        # Total Number of Units
        return Packs*size

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