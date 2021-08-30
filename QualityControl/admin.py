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

# Packing Materials
admin.site.register(PMParameters)
admin.site.register(PMSpecifications)
admin.site.register(PMSpecificationsItems)
admin.site.register(TempPMSpecifications)
admin.site.register(TempPMSpecificationsItems)
admin.site.register(PMSamples)
admin.site.register(PMAnalysis)
admin.site.register(PMAnalysisItems)
