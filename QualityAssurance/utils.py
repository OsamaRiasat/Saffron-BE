from QualityControl.models import ProductSamples
from Inventory.models import RMReceiving, PMReceiving
from datetime import date
from django.db.models import Max

def getQCNO():
    qcno=""
    try:
        print("in try")
        qcno=RMReceiving.objects.aggregate(Max('QCNo'))

        qcno=qcno['QCNo__max']
        no=int(qcno[5:])

        no=str(no+1)
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "R"+year+month+no
    except:
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "R"+year+month+"1"

    return qcno

def PMgetQCNO():
    qcno=""
    try:
        print("in try")
        qcno=PMReceiving.objects.aggregate(Max('QCNo'))
        print(qcno['QCNo__max'])
        qcno=qcno['QCNo__max']
        no=int(qcno[5:])
        no=str(no+1)
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "P"+year+month+no
    except:
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "P"+year+month+"1"

    return qcno

def FPgetQCNO():
    qcno=""
    try:
        qcno = ProductSamples.objects.aggregate(Max('QCNo'))
        print(qcno['QCNo__max'])
        qcno=qcno['QCNo__max']
        no=int(qcno[6:])
        no=str(no+1)
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "FP"+year+month+no
    except:
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "FP"+year+month+"1"

    return qcno