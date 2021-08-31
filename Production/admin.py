from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Stages)
admin.site.register(BatchIssuanceRequest)
admin.site.register(BPRLog)
admin.site.register(BatchStages)
admin.site.register(PackingLog)