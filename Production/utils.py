from .models import BPRLog, PMFormulation
from Products.models import Formulation
def CreateBatchNo(PCode):
    total = BPRLog.objects.values('batchNo').count()
    print(total)
    total = total+1
    batch_no = PCode+str(total)
    return batch_no

def getStandardBatchSize(PCode):
    batch_size = Formulation.objects.filter(ProductCode=PCode)
    size = None
    for i in batch_size:
        size = i.batchSize
    return size


def getStandardBatchSizePM(PCode, PackSize):
    batch_size = PMFormulation.objects.filter(ProductCode=PCode, PackSize=PackSize)
    size = None
    for i in batch_size:
        size = i.batchSize
    return size