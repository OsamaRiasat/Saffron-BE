from QualityControl.models import ProductSamples, RMSamples, PMSamples
from datetime import date
from django.db.models import Max

def getQCNO():
    qcno=""
    try:
        print("in try")
        max_date=RMSamples.objects.aggregate(Max('samplingDateTime'))
        max_date=max_date['samplingDateTime__max']
        qcno= RMSamples.objects.get(samplingDateTime__exact=max_date)
        qcno = qcno.QCNo
        no=int(qcno[5:])

        no=str(no+1)
        no=no.zfill(4)
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "R"+year+month+no
    except Exception as e:
        print("in except", e)
        today = date.today()
        year=str(today.year)
        year=year[2:]
        month=str(today.month)
        if len(month)==1:
            month="0"+month
        qcno = "R"+year+month+"0001"

    return qcno

def PMgetQCNO():
    qcno=""
    try:
        print("in try")
        qcno = PMSamples.objects.aggregate(Max('samplingDateTime'))
        qcno = qcno['samplingDateTime__max']
        qcno = PMSamples.objects.get(samplingDateTime__exact=qcno)
        qcno = qcno.QCNo
        no=int(qcno[5:])
        no=str(no+1)
        no=no.zfill(4)
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
        qcno = "P"+year+month+"0001"

    return qcno

def FPgetQCNO():
    qcno=""
    try:
        qcno = ProductSamples.objects.aggregate(Max('samplingDateTime'))
        qcno = qcno['samplingDateTime__max']
        qcno = ProductSamples.objects.get(samplingDateTime__exact=qcno)
        qcno = qcno.QCNo
        no=int(qcno[6:])
        no=str(no+1)
        no=no.zfill(4)
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
        qcno = "FP"+year+month+"0001"

    return qcno


