from rest_framework import serializers
from .models import *


# Suppliers

class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = ['S_ID', 'S_Name']
class SuppliersAllFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'

class SupplierApprovedItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierApprovedItems
        fields = '__all__'


class SupplierIDSsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierApprovedItems
        fields = ['S_ID']


class SupplierApprovedMCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierApprovedItems
        fields = ['MCode']

