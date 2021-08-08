from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response


# Products

class ProductViews(viewsets.ModelViewSet):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all()


class DosageFormsViews(viewsets.ModelViewSet):
    serializer_class = DosageFormsSerializer
    queryset = DosageForms.objects.all()


class PackSizesViews(viewsets.ModelViewSet):
    serializer_class = PackSizesSerializer
    queryset = PackSizes.objects.all()

