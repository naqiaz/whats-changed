'''
This file handles all logic related to authentication and signing up
'''
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout as auth_logout
def registerUser(request):
    '''
    registerUser goes hand-in-hand with signup. registerUser captures info from signup and adds the user to the database,
    then logs them in.
    '''

    #TODO: Render an actual template instead of HTTPResponse
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)

    verify = authenticate(username=username,password=password)
    if verify is not None:
        #The user is in the database, log them in
        print("asd")
    else:
        #The user is not in the database. Register them by creating a new user and adding to the database
        user = User.objects.create_user(username=username,password=password)


    return redirect('changed:index')
def auth(request):
    #authenticates and logs in the user
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)

    verify = authenticate(username=username,password=password)
    if verify is not None:
        #The user is in the database, log them in
        login(request,verify)
        print("Logged in successfully")
        context={
            'user':verify,
        }
        return render(request,'changed/home.html',context)
    else:
        #The user is not in the database. Register them by creating a new user and adding to the database
        #user = User.objects.create_user(username=username,password=password)
        return redirect('changed:index')

def logout(request):
    auth_logout(request)
    return redirect('changed:index')