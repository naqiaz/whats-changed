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
    if(Business.objects.filter(business_name=business_name).exists()):
        #the business already exists, don't create a duplicate
        print('The business already exists')
        business = Business.objects.get(business_name=business_name)
        business_info = BusinessInfo.objects.create(business=business, body = review_text)
        print(business_name)
        print(review_text)
        return redirect('changed:index')
    else:
        business = Business.objects.create(business_name=business_name)
        business_info = BusinessInfo.objects.create(business=business, body = review_text)
        print(business_name)
        print(review_text)
        return redirect('changed:index')
    

def show_reviews(request, business_id):
    #this page shows the respective business and all of its comments, shown when "Read review" is clicked
    try:
        business = Business.objects.get(id=business_id)
        business_name = business.business_name
        business_info = business.businessinfo_set.all()
        print(business_name)
        context = {
            'business':business,
            'business_info':business_info,
        }
        return render(request,'changed/comments.html',context)
        
    except:
        return render(request,'changed/home.html')

    
    
