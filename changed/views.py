from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo
from django.views.generic import DetailView

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
    business_pid=request.POST['businessPid']
    print(business_name)
    user = request.user
    if(Business.objects.filter(business_name=business_name,business_pid=business_pid).exists()):
        #the business already exists, don't create a duplicate
        print('The business already exists')
        business = Business.objects.get(business_name=business_name,business_pid=business_pid)
        user = User.objects.get(username=request.user.username)
        business_info = BusinessInfo.objects.create(business=business,user=user, body = review_text) 
        print(business_name)
        print(user.username)
        print(review_text)
        return redirect('changed:index')
    else:
        business = Business.objects.create(business_name=business_name,business_pid=business_pid)
        user = User.objects.get(username=request.user.username)
        business_info = BusinessInfo.objects.create(business=business, user=user,body = review_text)
        print(business_name)
        print(user.username)
        print(review_text)
        return redirect('changed:index')
    

def show_reviews(request):
    #this page shows the respective business and all of its comments, shown when "Read review" is clicked
        business_name = request.POST['businessName']
        business_pid = request.POST['businessPid']
        if (Business.objects.filter(business_name=business_name,business_pid=business_pid).exists()):
            business = Business.objects.get(business_name=business_name,business_pid=business_pid)
            business_name = business.business_name
            business_info = business.businessinfo_set.all()
            print(business_name) 
            context = {
            'business_name':business_name,
            'business_info':business_info,
            "business" : business,
            }
            return render(request,'changed/comments.html',context)
        else:
            return render(request,'changed/home.html')

def profile(request,username):
    #this page shows the respective profile and all of the user's reviews, when "profile" is clicked
        if (User.objects.filter(username=username).exists()):
            user = User.objects.get(username=username)
            username = user.username
            business_info = user.businessinfo_set.all()
            print(username) 
            context = {
            'user':user,
            'user_reviews':business_info,
            }
            return render(request,'changed/profile.html',context)
        else:
            return render(request,'changed/home.html')   

    
    
