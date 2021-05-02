from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MinValueValidator
import datetime

# Create your models here.

class Business(models.Model):
    business_name = models.TextField()
    business_pid = models.TextField()
    # the average COVID-19 Compliance rating, ranging from 0 to 5
    average_rating = models.FloatField(default=0.0)
    category = models.CharField(max_length = 50)
    def __str__(self):
        return self.business_name

    def average(self):
        # computes the average value based on submitted reviews
        reviews = BusinessInfo.objects.filter(business=self)
        rating = 0
        if len(reviews) > 0:
            for r in reviews:
                rating += r.covid_compliance_rating
            rating = rating/len(reviews)
            self.average_rating = rating
            self.save()
        return

class BusinessInfo(models.Model):
    # Business Reviews are specific to a particular business
    business = models.ForeignKey(Business, on_delete=models.CASCADE)

    # Business Reviews are also specific to the publishing user
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    # Covid Compliance Rating values range from 0 to 5
    covid_compliance_rating = models.IntegerField(default=5)

    # A capacity limit, can only contain positive integers
    capacity_limit = models.IntegerField(default=0)

    # A boolean field, based on whether or not indoor dining is available
    indoor_dining = models.BooleanField(default=False)

    # A boolean field based on whether or not oudoor dining is available
    outdoor_dining = models.BooleanField(default=False)

    # A boolean field based on whether or not curbisde pickup is available
    curbside_pickup = models.BooleanField(default=False)

    # A boolean field based on whether or not delivery is available
    delivery = models.BooleanField(default=False)

    # A text field for additional comments from users
    body = models.TextField(default="")

    published_date = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        businessinfo = self.business.business_name + ' '+str(self.covid_compliance_rating)
        return businessinfo

class Reply(models.Model):
    # replies are specific to a particular comment
    comment = models.ForeignKey(BusinessInfo, on_delete=models.CASCADE)

    # replies are also specific to the publishing user
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    body = models.TextField(default="")
    published_date = models.DateTimeField()
    def __str__(self):
        reply = self.body
        return reply

class BusinessForm(forms.Form):
    ################################################################################################################
    # REFERENCE
    # Title: Form Fields
    # URL: https://docs.djangoproject.com/en/3.2/ref/forms/fields/
    # Django Version: 3.2
    # Django License: BSD-3
    ################################################################################################################
   covid_compliance_rating = forms.TypedChoiceField(label="COVID Compliance Rating",choices=[(x,x) for x in range(1,6)],coerce=int,required=True)
   capacity_limit =forms.IntegerField(label="Capacity Limit",min_value=0,validators=[MinValueValidator(0)], required=True)
   indoor_dining = forms.BooleanField(label="Indoor Dining", required=False)
   outdoor_dining = forms.BooleanField(label="Outdoor Dining", required=False)
   curbside_pickup = forms.BooleanField(label="Curbside Pickup", required=False)
   delivery =forms.BooleanField(label="Delivery",required=False)
   body = forms.CharField(label="Additional Comments",widget=forms.Textarea,required=True)

class ReplyForm(forms.Form):
    reply = forms.CharField(label="Reply", widget=forms.Textarea,required=True)










