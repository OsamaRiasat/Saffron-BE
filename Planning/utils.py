



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