from django.db.models import fields
from rest_framework import serializers
from .models import *


# Raw Materials

class RawMaterialTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialTypes
        fields = '__all__'


class RawMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = '__all__'


class RawMaterialCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['RMCode', ]


class RawMaterialNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['Material', ]


class RawMaterialNameTypeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['Material', 'Type', 'Units', ]


class RawMaterialCodeTypeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['RMCode', 'Type', 'Units', ]


# Packing Materials

class PackingMaterialTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterialTypes
        fields = '__all__'


class PackingMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = '__all__'


class PackingMaterialCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode', ]


class PackingMaterialNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['Material', ]


class PackingMaterialNameTypeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['Material', 'Type', 'Units', ]


class PackingMaterialCodeTypeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode', 'Type', 'Units', ]


# RMDemands

class RMDemandItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMDemandedItems

        fields = ['RMCode', 'Priority', 'DemandedQty', ]


class RMDemandSerializer(serializers.ModelSerializer):
    demandedItems = RMDemandItemsSerializer(many=True, write_only=True)

    class Meta:
        model = RMDemands
        fields = ['demandedItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def create(self, validated_data):
        dItems = validated_data.pop('demandedItems')
        demand = RMDemands.objects.create(**validated_data)
        demand.save()

        for i in dItems:
            demands = RMDemandedItems.objects.create(DNo=demand, QuantityPending=i['DemandedQty'], RMCode=i['RMCode'],
                                                     Priority=i['Priority'],
                                                     DemandedQty=i['DemandedQty'])
            demands.save()
        return demand


class RMDemandsDNosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMDemands
        fields = ['DNo', ]


# PMDemands

class PMDemandItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMDemandedItems

        fields = ['PMCode', 'Priority', 'DemandedQty', ]


class PMDemandSerializer(serializers.ModelSerializer):
    demandedItems = PMDemandItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMDemands
        fields = ['demandedItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def create(self, validated_data):
        dItems = validated_data.pop('demandedItems')
        demand = PMDemands.objects.create(**validated_data)
        demand.save()

        for i in dItems:
            demands = PMDemandedItems.objects.create(DNo=demand, QuantityPending=i['DemandedQty'], PMCode=i['PMCode'],
                                                     Priority=i['Priority'],
                                                     DemandedQty=i['DemandedQty'])
            demands.save()
        return demand


class PMDemandsDNosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMDemands
        fields = ['DNo', ]


# RM Purchase Orders


class RMPurchaseOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMPurchaseOrderItems

        fields = ['SID', 'RMCode', 'Quantity']


class RMPurchaseOrdersSerializer(serializers.ModelSerializer):
    PO_ITEMS = RMPurchaseOrderItemsSerializer(many=True, write_only=True)

    class Meta:
        model = RMPurchaseOrders
        fields = ['DNo', 'PO_ITEMS', ]
        extra_kwargs = {
            'PONo': {'read_only': True},

        }

    def create(self, validated_data):
        pItems = validated_data.pop('PO_ITEMS')

        PO = RMPurchaseOrders.objects.create(**validated_data)
        PO.save()

        for i in pItems:
            PO_ITEM = RMPurchaseOrderItems.objects.create(PONo=PO,
                                                          SID=i['SID'],
                                                          RMCode=i['RMCode'],
                                                          Quantity=i['Quantity'],
                                                          Pending=i['Quantity'])
            PO_ITEM.save()

        return PO


class RMPurchaseOrderPONosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMPurchaseOrders
        fields = ['PONo', ]


class RMPurchaseOrderItemsRMCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMPurchaseOrderItems
        fields = ['RMCode', ]


# PM Purchase Orders


class PMPurchaseOrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMPurchaseOrderItems

        fields = ['SID', 'PMCode', 'Quantity']


class PMPurchaseOrdersSerializer(serializers.ModelSerializer):
    PO_ITEMS = PMPurchaseOrderItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMPurchaseOrders
        fields = ['DNo', 'PO_ITEMS', ]
        extra_kwargs = {
            'PONo': {'read_only': True},

        }

    def create(self, validated_data):
        pItems = validated_data.pop('PO_ITEMS')

        PO = PMPurchaseOrders.objects.create(**validated_data)
        PO.save()

        for i in pItems:
            PO_ITEM = PMPurchaseOrderItems.objects.create(PONo=PO,
                                                          SID=i['SID'],
                                                          PMCode=i['PMCode'],
                                                          Quantity=i['Quantity'],
                                                          Pending=i['Quantity'])
            PO_ITEM.save()

        return PO


class PMPurchaseOrderPONosSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMPurchaseOrders
        fields = ['PONo', ]


class PMPurchaseOrderItemsPMCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMPurchaseOrderItems
        fields = ['PMCode', ]


# RM Receiving

class RMIGPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['RMCode', 'quantityReceived', 'containersReceived', 'batchNo', 'PONo', 'S_ID']

    # def create(self, validated_data):
    #     # data = validated_data.pop(**validated_data)
    #     IGP = RMReceiving.objects.create(**validated_data)
    #     #IGP.save()
    #     print(IGP)
    #     # PO = RMPurchaseOrders.objects.create(**validated_data)
    #     # PO.save()
    #
    #     return IGP


# GRN

# class IGPNoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RMReceiving
#         fields = ['IGPNo', ]

# Generate GRN
class IGPNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['IGPNo', ]


class UpdateRMRecievingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['batchNo', 'quantityReceived', 'containersReceived', 'MFG_Date', 'EXP_Date', 'GRNo', 'remarks', ]

    def update(self, instance, validated_data):
        instance.batchNo = validated_data.get('batchNo', instance.batchNo)
        instance.quantityRecieved = validated_data.get('quantityReceived', instance.quantityReceived)
        instance.containersReceived = validated_data.get('containersReceived', instance.containersReceived)
        instance.MFG_Date = validated_data.get('MFG_Date', instance.MFG_Date)
        instance.EXP_Date = validated_data.get('EXP_Date', instance.EXP_Date)
        instance.GRNo = validated_data.get('GRNo', instance.GRNo)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        # instance.status = "QUARANTINED"
        instance.save()
        return instance


# POST GRN
class GRNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['GRNo', ]


class RMBinCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMBinCards
        fields = ['particulars', 'batchNo', 'received', 'QCNo', 'RMCode', ]


# PM Receiving

class PMIGPSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['PMCode', 'quantityReceived', 'containersReceived', 'batchNo', 'PONo', 'S_ID']

    # def create(self, validated_data):
    #     # data = validated_data.pop(**validated_data)
    #     IGP = RMReceiving.objects.create(**validated_data)
    #     #IGP.save()
    #     print(IGP)
    #     # PO = RMPurchaseOrders.objects.create(**validated_data)
    #     # PO.save()
    #
    #     return IGP


# GRN

# class IGPNoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RMReceiving
#         fields = ['IGPNo', ]

# Generate PM GRN
class PMIGPNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['IGPNo', ]


class UpdatePMRecievingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['batchNo', 'quantityReceived', 'containersReceived', 'MFG_Date', 'EXP_Date', 'GRNo', 'remarks', ]

    def update(self, instance, validated_data):
        instance.batchNo = validated_data.get('batchNo', instance.batchNo)
        instance.quantityRecieved = validated_data.get('quantityReceived', instance.quantityReceived)
        instance.containersReceived = validated_data.get('containersReceived', instance.containersReceived)
        instance.MFG_Date = validated_data.get('MFG_Date', instance.MFG_Date)
        instance.EXP_Date = validated_data.get('EXP_Date', instance.EXP_Date)
        instance.GRNo = validated_data.get('GRNo', instance.GRNo)
        instance.remarks = validated_data.get('remarks', instance.remarks)
        instance.status = "Under_Test"
        instance.save()
        return instance


# POST PM GRN
class PMGRNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['GRNo', ]


class PMBinCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMBinCards
        fields = ['particulars', 'batchNo', 'received', 'QCNo', 'PMCode', ]
