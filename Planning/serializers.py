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

        fields = ['ProductCode', 'PackSize', 'requiredPacks', 'inHandPacks', 'packsToBePlanned',
                  'noOfBatchesToBePlanned']


class PostPlanSerializer(serializers.ModelSerializer):
    planItems = PlanItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Plan
        fields = ['planItems', 'planNo']
        # extra_kwargs = {
        #     'DNo': {'read_only': True},
        #     'DDate': {'read_only': True},
        # }

    def create(self, validated_data):
        planNo = validated_data.get('planNo')
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
                                             noOfBatchesToBePlanned=i['noOfBatchesToBePlanned'],
                                             pendingPacks=i['packsToBePlanned'])
            items.save()
        return plan


class UpdatePlanSerializer(serializers.ModelSerializer):
    planItems = PlanItemsSerializer(many=True, write_only=True)

    class Meta:
        model = Plan
        fields = ('planItems', 'planNo')

    def update(self, instance, validated_data):

        planNo = instance.planNo
        plan = Plan.objects.get(planNo=planNo)
        data = PlanItems.objects.filter(planNo=planNo)
        for obj in data:
            obj.delete()
        pItems = validated_data.pop('planItems')
        for i in pItems:
            items = PlanItems.objects.create(planNo=plan,
                                             ProductCode=i['ProductCode'],
                                             PackSize=i['PackSize'],
                                             requiredPacks=i['requiredPacks'],
                                             inHandPacks=i['inHandPacks'],
                                             packsToBePlanned=i['packsToBePlanned'],
                                             noOfBatchesToBePlanned=i['noOfBatchesToBePlanned'],
                                             pendingPacks=i['packsToBePlanned'])
            items.save()

        message = "Updated"
        return message


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

#   -------------- PM Planning --------------

class ProductPackingMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPackingMaterials
        fields = '__all__'
