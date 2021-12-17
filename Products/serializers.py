from rest_framework import serializers

from Inventory.models import PackingMaterials
from Production.models import PMFormulation
from .models import *


# Products


# class ProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = '__all__'
#
#
# class PackSizesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PackSizes
#         fields = '__all__'
#
#
# class DosageFormsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DosageForms
#         fields = '__all__'
#
#
#
# class FormulationItemsSerializer(serializers.Serializer):
#     class Meta:
#         model = Formulation
#         fields = ['ProductCode', 'RMCode', 'batchSize', 'quantity', 'date', 'docNo']

# ------------      New Formulation    ------------------

class PCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductCode', ]


class PNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['Product', ]


class RMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawMaterials
        fields = ['RMCode', 'Material', 'Units', 'Type', ]


class FormulationItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formulation

        fields = ['ProductCode', 'RMCode', 'batchSize', 'quantity', 'date', 'docNo', ]


class FormulationSerializer(serializers.ModelSerializer):
    fItems = FormulationItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Formulation
        fields = ['fItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def validate(self, attrs):
        items = attrs.get('fItems')
        code = items[0]['ProductCode']
        check = Formulation.objects.filter(ProductCode=code)
        if check:
            check.delete()
        return attrs

    def create(self, validated_data):
        items = validated_data.pop('fItems')
        # demand = Formulation.objects.create(**validated_data)
        # demand.save()

        obj = ""
        for i in items:
            item = Formulation.objects.create(ProductCode=i['ProductCode'],
                                              RMCode=i['RMCode'],
                                              batchSize=i['batchSize'],
                                              quantity=i['quantity'],
                                              date=i['date'],
                                              docNo=i['docNo'])
            item.save()
            obj = i
        return obj


# ---------------- Add PackSize -----------------------

class ProductDataSerializer(serializers.ModelSerializer):
    DosageForm = serializers.CharField(source='dosageForm.dosageForm')

    class Meta:
        model = Products
        fields = ['Product', 'DosageForm', 'RegistrationNo']


class AddPackSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackSizes
        fields = '__all__'


# ------------      New PM Formulation    ------------------

class PMDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackingMaterials
        fields = ['PMCode', 'Material', 'Units', 'Type', ]


class PMFormulationItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMFormulation

        fields = ['ProductCode', 'PMCode', 'PackSize', 'batchSize', 'quantity', 'date', 'docNo', ]


class PMFormulationSerializer(serializers.ModelSerializer):
    fItems = PMFormulationItemsSerializer(many=True, write_only=True)

    class Meta:
        model = PMFormulation
        fields = ['fItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def validate(self, attrs):
        items = attrs.get('fItems')
        code = items[0]['ProductCode']
        check = PMFormulation.objects.filter(ProductCode=code)
        if check:
            check.delete()
        return attrs

    def create(self, validated_data):
        items = validated_data.pop('fItems')

        obj = ""
        for i in items:
            item = PMFormulation.objects.create(ProductCode=i['ProductCode'],
                                                 PMCode=i['PMCode'],
                                                 batchSize=i['batchSize'],
                                                 PackSize=i['PackSize'],
                                                 quantity=i['quantity'],
                                                 date=i['date'],
                                                 docNo=i['docNo'])
            item.save()
            obj = i
        return obj
