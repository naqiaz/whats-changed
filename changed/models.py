from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinValueValidator

# Create your models here.

class Business(models.Model):
    business_name = models.TextField()
    business_pid = models.TextField()
    #average_compliance_rating = models.IntegerField()
    category = models.CharField(max_length = 50)
    def __str__(self):
        return self.business_name

class BusinessInfo(models.Model):
    #Business info relies on the 
    business = models.ForeignKey(Business, on_delete=models.CASCADE) 
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    #Rating goes from 1-5
    covid_compliance_rating = models.IntegerField(default=5)
    capacity_limit = models.IntegerField(default=0)
    indoor_dining = models.BooleanField(default=False)
    outdoor_dining = models.BooleanField(default=False)
    curbside_pickup = models.BooleanField(default=False)
    delivery = models.BooleanField(default=False)
    body = models.TextField(default="")
    def __str__(self):
        businessinfo = self.business.business_name + ' '+str(self.covid_compliance_rating)
        return businessinfo
class Reply(models.Model):
    comment = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField(default="")
    def __str__(self):
        reply = self.body
        return reply
class BusinessForm(forms.Form):
   covid_compliance_rating = forms.TypedChoiceField(label="COVID Compliance Rating",choices=[(x,x) for x in range(1,6)],coerce=int,required=False)
   capacity_limit =forms.IntegerField(label="Capacity Limit",validators=[MinValueValidator(0)], required=False)
   indoor_dining = forms.BooleanField(label="Indoor Dining", required=False)
   outdoor_dining = forms.BooleanField(label="Outdoor Dining", required=False)
   curbside_pickup = forms.BooleanField(label="Curbside Pickup", required=False)
   delivery =forms.BooleanField(label="Delivery",required=False)
   body = forms.CharField(label="Additional Comments",widget=forms.Textarea,required=False)
class ReplyForm(forms.Form):
    reply = forms.CharField(label="Reply", widget=forms.Textarea)




