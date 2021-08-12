from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(RawMaterials)
admin.site.register(RawMaterialTypes)
admin.site.register(RMDemands)
admin.site.register(RMDemandedItems)
admin.site.register(RMPurchaseOrders)
admin.site.register(RMPurchaseOrderItems)
admin.site.register(RMReceiving)
admin.site.register(RMBinCards)

admin.site.register(PackingMaterials)
admin.site.register(PackingMaterialTypes)
admin.site.register(PMDemands)
admin.site.register(PMDemandedItems)
admin.site.register(PMPurchaseOrders)
admin.site.register(PMPurchaseOrderItems)
admin.site.register(PMReceiving)
admin.site.register(PMBinCards)
