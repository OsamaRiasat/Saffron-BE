from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *

router = DefaultRouter()

# Suppliers

urlpatterns = [
    path('suppliers', suppliers.as_view())

]
