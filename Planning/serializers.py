from rest_framework import serializers
from .models import *


 # A-Product Selection

class ProductNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['Product', ]

class ProductCodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['ProductCode', ]



class PlanItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanItems

        fields = [ 'ProductCode', 'PackSize', 'requiredPacks', 'inHandPacks', 'packsToBePlanned', 'noOfBatchesToBePlanned' ]


class PostPlanSerializer(serializers.ModelSerializer):
    planItems = PlanItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Plan
        fields = ['planItems', ]
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def create(self, validated_data):
        pItems = validated_data.pop('planItems')
        plan = Plan.objects.create(**validated_data)
        plan.save()

        for i in pItems:
            items = PlanItems.objects.create(planNo=plan,
                                             ProductCode=i['ProductCode'],
                                             PackSize=i['PackSize'],
                                             requiredPacks=i['requiredPacks'],
                                             inHandPacks=i['inHandPacks'],
                                             packsToBePlanned=i['packsToBePlanned'],
                                             noOfBatchesToBePlanned=i['noOfBatchesToBePlanned'] ,
                                             pendingPacks=i['packsToBePlanned'])
            items.save()
        return plan
