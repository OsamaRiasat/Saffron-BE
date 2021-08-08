from .models import *
from Inventory.models import RawMaterials


def approvedItems(SID):
    data = SupplierApprovedItems.objects.filter(S_ID=SID)  # This will give objects of approved items having this SID
    l = []
    for obj in data:
        dic = {}
        Materials = RawMaterials.objects.filter(pk=obj.MCode).only('Material')
        dic["Material"] = Materials.get().Material
        l.append(dic)
    return l


def supplierApprovedItemsCodesList(SID):
    data = SupplierApprovedItems.objects.filter(S_ID=SID)  # This will give objects of approved items having this SID
    l=[]
    for obj in data:
        code = obj.MCode
        l.append(code)
    return l
