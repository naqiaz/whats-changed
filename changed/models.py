from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Business(models.Model):
    business_name = models.TextField()
    business_pid = models.TextField()
    category = models.CharField(max_length = 50)
    def __str__(self):
        return self.business_name

class BusinessInfo(models.Model):
    #Business info relies on the 
    business = models.ForeignKey(Business, on_delete=models.CASCADE) 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #Rating goes from 1-5
    covid_compliance_rating = models.IntegerField(default=5)
    body = models.TextField(default="")
    def __str__(self):
        businessinfo = self.business.business_name + ' '+str(self.covid_compliance_rating)
        return businessinfo




