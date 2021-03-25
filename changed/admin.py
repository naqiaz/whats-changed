from django.contrib import admin
from .models import Business, BusinessComments, BusinessInfo
# Register your models here.
admin.site.register(Business)
admin.site.register(BusinessComments)
admin.site.register(BusinessInfo)
