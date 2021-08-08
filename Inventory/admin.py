from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(RawMaterials)
admin.site.register(RawMaterialTypes)
admin.site.register(PackingMaterials)
admin.site.register(PackingMaterialTypes)
admin.site.register(RMDemands)
admin.site.register(RMDemandedItems)
admin.site.register(RMPurchaseOrders)
admin.site.register(RMPurchaseOrderItems)
admin.site.register(RMReceiving)
admin.site.register(RMBinCards)