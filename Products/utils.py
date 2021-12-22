from .models import *

def getName(PCode):
    print(type(PCode))
    name = Products.objects.get(ProductCode=PCode).Product
    dic = {}
    dic['Product'] = name
    return dic

def getCode(Pname):
    dic = {}
    try:
        pcode = Products.objects.get(Product=Pname).ProductCode
        dic['ProductCode'] = pcode
    except:
        dic["error"] = "Not Exists"


    return dic