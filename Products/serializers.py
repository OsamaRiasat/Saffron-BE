from rest_framework import serializers
from .models import *


# Products

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class PackSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackSizes
        fields = '__all__'


class DosageFormsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DosageForms
        fields = '__all__'

