from django.contrib import admin
from .models import *
# Register your models here.

# Raw Materials
admin.site.register(RMParameters)
admin.site.register(RMReferences)
admin.site.register(RMSpecifications)
admin.site.register(RMSpecificationsItems)
admin.site.register(TempRMSpecifications)
admin.site.register(TempRMSpecificationsItems)
admin.site.register(RMSamples)
admin.site.register(RMAnalysis)
admin.site.register(RMAnalysisItems)
admin.site.register(RMAnalysisLog)
admin.site.register(RMAnalysisItemsLog)

# Packing Materials
admin.site.register(PMParameters)
admin.site.register(PMSpecifications)
admin.site.register(PMSpecificationsItems)
admin.site.register(TempPMSpecifications)
admin.site.register(TempPMSpecificationsItems)
admin.site.register(PMSamples)
admin.site.register(PMAnalysis)
admin.site.register(PMAnalysisItems)


# Products
admin.site.register(ProductParameters)
admin.site.register(ProductSpecifications)
admin.site.register(ProductSpecificationsItems)
admin.site.register(TempProductSpecifications)
admin.site.register(TempProductSpecificationsItems)
admin.site.register(ProductSamples)
admin.site.register(ProductAnalysis)
admin.site.register(ProductAnalysisItems)
