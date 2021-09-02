from django.db.models import fields
from .views import *
from rest_framework import serializers
from Inventory.models import RMReceiving, PMReceiving
from QualityControl.models import RMSamples, PMSamples
from .utils import getQCNO, PMgetQCNO


#  -------------------- RM SAMPLES --------------------

class GRNOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RMReceiving
        fields = ['GRNo', ]


class RMSampleSerializer(serializers.ModelSerializer):
    GRNo = serializers.IntegerField(write_only=True)

    class Meta:
        model = RMSamples
        fields = ['QCNo', 'GRNo', 'deliveredBy', 'receivedBy', ]

    def create(self, validated_data):
        grno = validated_data['GRNo']
        qcno = getQCNO()
        receiving = RMReceiving.objects.filter(GRNo=grno).first()
        rm = RMSamples.objects.create(
            QCNo=qcno,
            IGPNo=receiving,
            deliveredBy=validated_data['deliveredBy'],
            receivedBy=validated_data['receivedBy']
        )
        rm.save()
        receiving.QCNo = qcno
        receiving.status = 'UNDER_TEST'
        receiving.save()
        return rm


#  -------------------- PM SAMPLES --------------------

class PMGRNOListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMReceiving
        fields = ['GRNo', ]


class PMSampleSerializer(serializers.ModelSerializer):
    GRNo = serializers.IntegerField(write_only=True)

    class Meta:
        model = PMSamples
        fields = ['QCNo', 'GRNo', 'deliveredBy', 'receivedBy', ]

    def create(self, validated_data):
        grno = validated_data['GRNo']
        qcno = getQCNO()
        receiving = PMReceiving.objects.filter(GRNo=grno).first()
        rm = PMSamples.objects.create(
            QCNo=qcno,
            IGPNo=receiving,
            deliveredBy=validated_data['deliveredBy'],
            receivedBy=validated_data['receivedBy']
        )
        rm.save()
        receiving.QCNo = qcno
        receiving.status = 'UNDER_TEST'
        receiving.save()
        return rm
