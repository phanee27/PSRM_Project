from django.shortcuts import render

# Create your views here.

def hompage(request):
    return render(request,'adminApp/homepage.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Registration and Login View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from tenentapp.models import TenentUser
from django.contrib.auth.hashers import make_password  # To hash the password

def login_or_register(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            # Registration Logic
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            # Check if the username already exists in auth_user
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            else:
                # Save the user in the Django User table (auth_user)
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # Also save the user in the TenentUser table
                tenent_user = TenentUser.objects.create(
                    user=user,
                    username=username,
                    email=email,
                    password=make_password(password)  # Hash the password for security
                )
                tenent_user.save()

                messages.success(request, 'Registration successful! Please log in.')
                return redirect('adminapp:login_or_register')  # Redirect to the same page for login

        elif 'login' in request.POST:
            # Login Logic
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Check if the username and password are both 'admin'
                if username == 'admin' and password == 'admin':
                    return redirect('adminapp:homepage1')  # Redirect to adminapp homepage
                else:
                    return redirect('tenentapp:tenenthomepage')  # Redirect to tenentapp homepage
            else:
                messages.error(request, 'Invalid username or password')

    return render(request, 'adminApp/loginpage.html')


# Logout View
def logout_view(request):
    logout(request)
    return redirect('tenentapp:tenenthomepage')


@login_required
def homepage1(request):
    return render(request, 'adminApp/homepage.html', {'username': request.user.username})

