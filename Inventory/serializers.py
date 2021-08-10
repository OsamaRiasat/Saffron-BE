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


# RM Receiving

class RMIGPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['RMCode', 'quantityReceived', 'containersReceived', 'batchNo', 'PONo','S_ID']

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

class IGPNoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['IGPNo', ]