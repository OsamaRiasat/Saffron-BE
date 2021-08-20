from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
from .models import *
# Create your views here.




#Populate Database



class PopulateParametersView(APIView):
    def get(self,request):
        workbook = pd.read_excel(r'C:\Users\usama riasat\Documents\Saffron-Clones\Saffron-Restful-APIs\SaffronProject\QualityControl\parameters.xlsx ',sheet_name='Sheet1')
        workbook=workbook.to_numpy()

        for i in workbook:
            t=str(i[0])
            print(t)
            paramater1 =RMParameters.objects.create(parameter=i[0])
            paramater1.save()

        return Response({"Populate":"Done"})
