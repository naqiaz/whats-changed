from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Business(models.Model):
    business_name = models.TextField()
    category = models.CharField(max_length = 50)

class BusinessInfo(models.Model):
    #Business info relies on the 
    business = models.ForeignKey(Business, on_delete=models.CASCADE) 
    #Rating goes from 1-5
    covid_compliance_rating = models.IntegerField(default=5)

#a business can have multiple comments from a variety of users
class BusinessComments(models.Model):
    #grabs the user who made the comment
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    business_info = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE)
    body = models.TextField()




