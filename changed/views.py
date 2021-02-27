from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    #the default page is the login page
    return render(request,'changed/login.html')

def auth(request):
    username = request.POST['username']
    password = request.POST['password']
    print(username)
    print(password)

    verify = authenticate(username=username,password=password)
    if verify is not None:
        #The user is in the database, log them in
        login(request,verify)
        print("Logged in successfully")
    else:
        #The user is not in the database. Register them by creating a new user and adding to the database
        user = User.objects.create_user(username=username,password=password)

    return HttpResponse("asdasdasd")

def signup(request):
    return render(request,'changed/signup.html')
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


    return HttpResponse("testingtesting123")