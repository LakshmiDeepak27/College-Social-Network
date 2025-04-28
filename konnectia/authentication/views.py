from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def homePage(request):
    return render(request , "homePage.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        cpassword = request.POST['pass2']

        myuser= User.objects.create_user(username,password,email) 
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        messages.success(request , "Your account has been created successfully")
        return redirect('signin')
    return render(request , "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username , password=password)

        if user is not None:
            login(request , user)
            # messages.success(request , "You have been logged in successfully")
            return render(request , "konnecita/authentication/templates/authentication/index. html")
        
        else:
            messages.error(request , "Invalid credentials, please try again")
            return redirect('home')


    return render(request , "authentication/signin.html")

def signout(request):
    pass