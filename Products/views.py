from django.shortcuts import render
from rest_framework import viewsets, generics
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response



class FormulationsView(generics.CreateAPIView):
    serializer_class = FormulationSerializer
    queryset = Formulation.objects.all()
