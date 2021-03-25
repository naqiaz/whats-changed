from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo, BusinessComments

# Create your views here.
def index(request):
    if request.user.is_authenticated:
            return render(request,'changed/home.html')
    else:
            return render(request,'changed/login.html')

def signup(request):
    return render(request,'changed/signup.html')

def business_review_list(request):
        #shows the reviews for a business (when you click 'Read review')
    return HttpResponse('Somebody write a reviews list')

def writeReview(request):
    '''
    TODO: Business = business_name, BusinessInfo = covid_compliance_rating
    '''
    review_text = request.POST['review-text']
    business_name=request.POST['businessName']
    user = request.user
    business = Business.objects.create(business_name=business_name)
    business_info = BusinessInfo.objects.create(business=business)
    business_comment = BusinessComments.objects.create(user=user,business_info=business_info,body=review_text)
    print(business_name)
    print(review_text)
    return HttpResponse("This is a test of writeReview")
    
