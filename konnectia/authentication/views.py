from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from konnectia import settings
from django.contrib.sites.shortcuts import get_current_site

from django.utils.http import urlsafe_base64_encode , urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .tokens import generate_token
# Create your views here.

from django.contrib.auth import get_user_model  
User = get_user_model() 

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


        if  User.objects.filter(username=username).exists():
            messages.error(request , "Username already exists.Please try some other username")
            return redirect('home')
        

        if  User.objects.filter(email=email).exists():
            messages.error(request , "Email already exists.Please try some other email")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request , "Username must be under 10 characters")
            # return redirect('home')
        
        if password != cpassword:
            messages.error(request , "Password do not match")
            # return redirect('home')
        
        if not username.isalnum():
            messages.error(request , "Username should only contain letters and numbers")
            return redirect('home')

        myuser= User.objects.create_user(username,email,password) 
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.is_active = False  # Deactivate account until email is confirmed
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

        
        # Send confirmation email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ KONNECTIA!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')


    return render(request , "authentication/signup.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request, 'activation_failed.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass1']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have been logged in successfully")
                return render(request, "authentication/index.html")
            else:
                messages.error(request, "Your account is not activated. Please check your email for the activation link.")
                return render(request, "authentication/signin.html")
        else:
            messages.error(request, "Invalid credentials, please try again")
            return render(request, "authentication/signin.html")

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect('home')
