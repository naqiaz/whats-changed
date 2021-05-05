from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
from .models import Business, BusinessInfo, Reply
from .models import BusinessForm, ReplyForm
from django.views.generic import DetailView
from datetime import datetime, timedelta
from django.http import JsonResponse

def index(request):
    # if the user is authenticated, render the home page 
    if request.user.is_authenticated:
            form = BusinessForm()
            return render(request,'changed/home.html',{'form':form})
    # if the user is not authenticated, render the login page
    else:
            form = BusinessForm()
            return render(request,'changed/login.html',{'form':form})

def rating(request):
    ################################################################################################################
    # REFERENCE
    # Title: How to Work with Ajax Request with Django
    # Author: Vitor Freitas
    # URL: https://simpleisbetterthancomplex.com/tutorial/2016/08/29/how-to-work-with-ajax-request-with-django.html
    # Django License: BSD-3
    ################################################################################################################
    name = request.GET['name']
    pid = request.GET['pid']
    if (Business.objects.filter(business_name=name,business_pid=pid).exists()):
        business = Business.objects.get(business_name=name,business_pid=pid)
        rating = business.average_rating
        rating = round(rating, 1)
        business_info = business.businessinfo_set.all().order_by('-published_date')
        business_info = business_info.first()
        if (business_info != None):
            capacity_limit = business_info.capacity_limit
            published_date = business_info.published_date 
            published_date = published_date.strftime('%Y-%m-%d %H:%M')
            published_date = "Latest review: " + published_date
        else:
            capacity_limit = "No reviews"
            published_date = "No reviews"
    else:
        rating = ""
        capacity_limit = "No reviews"
        published_date = "No reviews"
    data = {
        'pid':pid,
        'rtg': rating,
        'published_date':published_date,
        'capacity_limit':capacity_limit,
    }
    return JsonResponse(data)

def about(request):
    # renders the view for an about page, which can be viewed even if a user is not authenticated
      return render(request,'changed/about.html')


def signup(request):
    # renders the view for a sign up page, with a form
    return render(request,'changed/signup.html')


def writeReview(request):
    # handles the submission of a business review
    if request.method == 'POST':
        form = BusinessForm(request.POST)
        if form.is_valid():
            business_name = request.POST['businessName']
            business_pid = request.POST['businessPid']
            covid_compliance_rating = form.cleaned_data['covid_compliance_rating']
            capacity_limit = form.cleaned_data['capacity_limit']
            indoor_dining = form.cleaned_data['indoor_dining']
            outdoor_dining = form.cleaned_data['outdoor_dining']
            curbside_pickup = form.cleaned_data['curbside_pickup']
            delivery = form.cleaned_data['delivery']
            body = form.cleaned_data['body']
            published_date = datetime.now() + timedelta(hours=-4)

            # if the business exists do not create a duplicate
            if(Business.objects.filter(business_name=business_name,business_pid=business_pid).exists()):
                business = Business.objects.get(business_name=business_name,business_pid=business_pid)
                user = User.objects.get(username=request.user.username)
                business_info = BusinessInfo.objects.create(business=business,user=user, covid_compliance_rating=covid_compliance_rating,capacity_limit=capacity_limit,
                                                           indoor_dining=indoor_dining,outdoor_dining=outdoor_dining, curbside_pickup=curbside_pickup,delivery=delivery,body = body,
                                                           published_date = published_date)
                business.average()
                return HttpResponseRedirect(reverse('changed:index'))

            # else create a new business object and a comment object
            else:
                business = Business.objects.create(business_name=business_name,business_pid=business_pid,average_rating=0)
                user = User.objects.get(username=request.user.username)
                business_info = BusinessInfo.objects.create(business=business,user=user, covid_compliance_rating=covid_compliance_rating,capacity_limit=capacity_limit,
                                                           indoor_dining=indoor_dining,outdoor_dining=outdoor_dining, curbside_pickup=curbside_pickup,delivery=delivery,body = body,
                                                           published_date=published_date)
                business.average()
                return HttpResponseRedirect(reverse('changed:index'))
        return HttpResponseRedirect(reverse('changed:index'))
    else:
        form = BusinessForm()
        return render(request,'changed/home.html',{'form':form})


def show_reviews(request):
    # this page shows the respective business and all of its comments, shown when "Read review" is clicked
        business_name = request.POST['businessName']
        business_pid = request.POST['businessPid']

        if (Business.objects.filter(business_name=business_name,business_pid=business_pid).exists()):
            business = Business.objects.get(business_name=business_name,business_pid=business_pid)
            avg_rating = business.average_rating
            avg_rating = round(avg_rating,1)
            business_name = business.business_name
            business_info = business.businessinfo_set.all().order_by('-published_date')
            editForm = BusinessForm()
            context = {
            'business_name':business_name,
            'avg_rating': avg_rating,
            'business_info':business_info,
            "business" : business,
            'editForm': editForm,
            }
            return render(request,'changed/comments.html',context)
        else:
            form = BusinessForm()
            return render(request,'changed/home.html',{'form':form})

def profile(request,username):
    # this page shows the respective profile and all of the user's reviews, when "profile" is clicked
        if (User.objects.filter(username=username).exists()):
            user = request.user
            business_info = user.businessinfo_set.all().order_by('-published_date')
            editForm = BusinessForm()
            context = {
            'user':user,
            'user_reviews':business_info,
            'editForm':editForm,
            }
            return render(request,'changed/profile.html',context)
        else:
            form = BusinessForm()
            return render(request,'changed/home.html',{'form':form})  

def reply(request,id):
    # this page shows all the replies to a specific comment, and handles the submission of new replies
        if (BusinessInfo.objects.filter(id=id).exists()):
            comment = BusinessInfo.objects.get(id=id)
            replies = comment.reply_set.all().order_by('-published_date') 
            form = ReplyForm()
            editForm = ReplyForm()
            context = {
            'comment':comment,
            'replies':replies,
            'form':form,
            'editForm':editForm,
            }
            # if a reply is submitted create a new reply object
            if request.method == 'POST':
              form = ReplyForm(request.POST)
              if form.is_valid():
                reply = form.cleaned_data['reply']
                user = request.user
                published_date = datetime.now() + timedelta(hours=-4)
                reply = Reply.objects.create(body=reply,comment=comment,user=user,published_date=published_date)
            return render(request,'changed/replies.html',context)   
        else:
            form = BusinessForm()
            return render(request,'changed/home.html',{'form':form})

def delete_reply(request,comment_id, reply_id):
    # handles a request to delete a reply object
        if (Reply.objects.filter(id=reply_id).exists()):
            reply = Reply.objects.filter(id=reply_id).delete()
        comment = BusinessInfo.objects.get(id=comment_id)
        replies = comment.reply_set.all().order_by('-published_date')
        form = ReplyForm()
        editForm = ReplyForm()
        context ={
            'comment':comment,
            'replies':replies,
            'form':form,
            'editForm':editForm
             }
        return render(request,'changed/replies.html',context)

def edit_reply(request,comment_id, reply_id):
    # handles a request to update a reply object
    reply = Reply.objects.get(id=reply_id)
    comment = BusinessInfo.objects.get(id=comment_id)
    replies = comment.reply_set.all().order_by('-published_date')
    editForm = ReplyForm()
    form = ReplyForm()
    context ={
            'comment':comment,
            'replies':replies,
            'form':form,
            'editForm':editForm,
             }
    if request.method == 'POST':
       editForm = ReplyForm(request.POST)
       if editForm.is_valid():
          reply.body = editForm.cleaned_data['reply']
          reply.save()
    return render(request,'changed/replies.html',context)

def delete_comment(request,business_pid,comment_id):
    # handles a request to delete a comment object
    if (BusinessInfo.objects.filter(id=comment_id).exists()):
        BusinessInfo.objects.filter(id=comment_id).delete()
    business = Business.objects.get(business_pid=business_pid)
    business.average()
    avg_rating = round(business.average_rating,1)
    business_info = business.businessinfo_set.all().order_by('-published_date') 
    editForm = BusinessForm()
    context = {
       'business_name':business.business_name,
       'avg_rating': avg_rating,
       'business_info':business_info,
       'business' : business,
       'editForm' : editForm
    }
    return render(request,'changed/comments.html',context)

def edit_comment(request,business_pid,comment_id):
    # handles a request to update a comment object
    comment = BusinessInfo.objects.get(id=comment_id)
    business = Business.objects.get(business_pid=business_pid)
    business_info = business.businessinfo_set.all().order_by('-published_date') 
    if request.method == 'POST':
        editForm = BusinessForm(request.POST)
        if editForm.is_valid():
            comment.covid_compliance_rating = editForm.cleaned_data['covid_compliance_rating']
            comment.capacity_limit = editForm.cleaned_data['capacity_limit']
            comment.indoor_dining = editForm.cleaned_data['indoor_dining']
            comment.outdoor_dining = editForm.cleaned_data['outdoor_dining']
            comment.curbside_pickup = editForm.cleaned_data['curbside_pickup']
            comment.delivery = editForm.cleaned_data['delivery']
            comment.body = editForm.cleaned_data['body']
            comment.published_date = comment.published_date
            comment.save()
            business.average()
    editForm = BusinessForm()
    context = {
       'business_name':business.business_name,
       'avg_rating': business.average_rating,
       'business_info':business_info,
       'business' : business,
       'editForm': editForm,
    }
    return render(request,'changed/comments.html',context)

def delete_comment_prof(request,business_pid,comment_id):
    # handles a request to delete a comment object from the profile page
    if (BusinessInfo.objects.filter(id=comment_id).exists()):
        BusinessInfo.objects.filter(id=comment_id).delete()
        business = Business.objects.get(business_pid=business_pid)
        business.average()
    # After comment has been deleted, render the profile page
    user = request.user
    business_info = user.businessinfo_set.all().order_by('-published_date')
    editForm = BusinessForm()
    context = {
            'user':user,
            'user_reviews':business_info,
            'editForm':editForm,
            }
    return render(request,'changed/profile.html',context)

def edit_comment_prof(request,business_pid,comment_id):
    # handles a request to update a comment object from the profile page
    comment = BusinessInfo.objects.get(id=comment_id)
    business = Business.objects.get(business_pid=business_pid)
    if request.method == 'POST':
        editForm = BusinessForm(request.POST)
        if editForm.is_valid():
            comment.covid_compliance_rating = editForm.cleaned_data['covid_compliance_rating']
            comment.capacity_limit = editForm.cleaned_data['capacity_limit']
            comment.indoor_dining = editForm.cleaned_data['indoor_dining']
            comment.outdoor_dining = editForm.cleaned_data['outdoor_dining']
            comment.curbside_pickup = editForm.cleaned_data['curbside_pickup']
            comment.delivery = editForm.cleaned_data['delivery']
            comment.body = editForm.cleaned_data['body']
            comment.published_date = comment.published_date
            comment.save()
            business.average()
    # After comment has been updated, render the profile page
    user = request.user
    business_info = user.businessinfo_set.all().order_by('-published_date')
    editForm = BusinessForm()
    context = {
            'user':user,
            'user_reviews':business_info,
            'editForm':editForm,
            }
    return render(request,'changed/profile.html',context)  
