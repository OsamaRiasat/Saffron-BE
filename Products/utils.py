
from .models import *

def getName(PCode):
    print(type(PCode))
    name = Products.objects.get(ProductCode=PCode).Product
    dic = {}
    dic['Product'] = name
    return dic

def getCode(Pname):
    pcode = Products.objects.get(Product=Pname).ProductCode
    dic = {}
    dic['ProductCode'] = pcode
    return dic