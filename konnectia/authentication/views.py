from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from konnectia import settings
# Create your views here.

def homePage(request):
    return render(request, "homePage.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass1']
        cpassword = request.POST['pass2']


        # if  User.objects.filter(username=username).exists():
        #     messages.error(request , "Username already exists.Please try some other username")
        #     return redirect('home')
        

        # if  User.objects.filter(eamil=email).exists():
        #     messages.error(request , "Email already exists.Please try some other email")
        #     return redirect('home')
        
        # if (username)>10:
        #     messages.error(request , "Username must be under 10 characters")
        #     # return redirect('home')
        
        # if password != cpassword:
        #     messages.error(request , "Password do not match")
        #     # return redirect('home')
        
        # if not username.isalnum():
        #     messages.error(request , "Username should only contain letters and numbers")
        #     return redirect('home')

        myuser= User.objects.create_user(username,email,password) 
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        # Send welcome email
        subject = "Welcome to Konnectia"
        message = f"Hello {myuser.first_name}!!\nWelcome to Konnectia!!\nThank you for visiting our website\nWe have also sent you a confirmation email, please confirm your email address in order to activate your account\n\nThank you for visiting our website\nWe hope you have a great experience with us.\n\nRegards\nKonnectia"
        from_email = settings.EMAIL_HOST_USER       
        to_list = [myuser.email]
        
        try:
            send_mail(subject, message, from_email, to_list, fail_silently=False)
            messages.success(request, "Your account has been created successfully. We have sent you a confirmation email.")
        except Exception as e:
            messages.error(request, f"Account created but email could not be sent: {str(e)}")

        return redirect('signin')


    return render(request , "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username , password=password)

        if user is not None:
            login(request , user)
            messages.success(request , "You have been logged in successfully")
            # return render(request, "authentication/signin.html")
            return render(request, "authentication/index.html")
        
        else:
            messages.error(request , "Invalid credentials, please try again")
            return redirect('home')
            



    return render(request , "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request , "You have been logged out successfully")
    return redirect('home')