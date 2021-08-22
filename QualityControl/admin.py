from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(RMParameters)
admin.site.register(RMReferences)
admin.site.register(RMSpecifications)
admin.site.register(RMSpecificationsItems)

admin.site.register(PMParameters)
admin.site.register(PMSpecifications)
admin.site.register(PMSpecificationsItems)

admin.site.register(ProductParameters)
admin.site.register(ProductSpecifications)
admin.site.register(ProductSpecificationsItems)