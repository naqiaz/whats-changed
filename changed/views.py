from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo

# Create your views here.
def index(request):
    if request.user.is_authenticated:
            return render(request,'changed/home.html')
    else:
            return render(request,'changed/login.html')

def signup(request):
    return render(request,'changed/signup.html')


def writeReview(request):
    '''
    TODO: Business = business_name, BusinessInfo = covid_compliance_rating
    '''
    review_text = request.POST['review-text']
    business_name=request.POST['businessName']
    business_addr = request.POST['addr']
    user = request.user
    if(Business.objects.filter(business_name=business_name, business_addr=business_addr).exists()):
        #the business already exists, don't create a duplicate
        print('The business already exists')
        business = Business.objects.get(business_name=business_name,business_addr=business_addr)
        business_info = BusinessInfo.objects.create(business=business, body = review_text)
        print(business_name)
        print(review_text)
        print(business_addr)
        return redirect('changed:index')
    else:
        business = Business.objects.create(business_name=business_name,business_addr=business_addr)
        business_info = BusinessInfo.objects.create(business=business, body = review_text)
        print(business_name)
        print(review_text)
        print(business_addr)
        return redirect('changed:index')
    

def show_reviews(request):
    #this page shows the respective business and all of its comments, shown when "Read review" is clicked
        business_name = request.POST['businessName']
        if (Business.objects.filter(business_name=business_name).exists()):
            business = Business.objects.get(business_name=business_name)
            business_name = business.business_name
            business_info = business.businessinfo_set.all()
            print(business_name) 
            context = {
            'business':business,
            'business_info':business_info,
            }
            return render(request,'changed/comments.html',context)
        else:
            return render(request,'changed/home.html')

    
    
