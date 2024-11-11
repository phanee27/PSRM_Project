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



from django.shortcuts import render, get_object_or_404, redirect
from ownerapp.models import OwnerUser
from tenentapp.models import TenentUser


# Dashboard view to display Owners and Tenants
def dashboard(request):
    owners = OwnerUser.objects.all()
    tenants = TenentUser.objects.all()
    context = {
        'owners': owners,
        'tenants': tenants
    }
    return render(request, 'adminapp/Dashboard.html', context)

# Other views can remain the same for editing and deleting owners and tenants if needed


# Edit Owner
# adminapp/views.py
from django.contrib.auth.models import User

# Edit Owner View
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from ownerapp.models import OwnerUser
from django.contrib import messages

def edit_owner(request, owner_id):
    owner = get_object_or_404(OwnerUser, id=owner_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if User.objects.exclude(id=owner.user.id).filter(username=new_username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'adminApp/edit_owner.html', {'owner': owner})

        # Update OwnerUser model
        owner.username = new_username
        owner.email = new_email
        owner.save()

        # Update the associated auth_user entry
        user = User.objects.get(id=owner.user.id)
        user.username = new_username
        user.email = new_email
        user.save()

        # messages.success(request, "Owner updated successfully.")
        return redirect('adminapp:dashboard')

    return render(request, 'adminApp/edit_owner.html', {'owner': owner})


# Edit Tenant View


def edit_tenant(request, tenant_id):
    tenant = get_object_or_404(TenentUser, id=tenant_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        if User.objects.exclude(id=tenant.user.id).filter(username=new_username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return render(request, 'adminApp/edit_tenent.html', {'tenant': tenant})

        # Update TenantUser model
        tenant.username = new_username
        tenant.email = new_email
        tenant.save()

        # Update the associated auth_user entry
        user = User.objects.get(id=tenant.user.id)
        user.username = new_username
        user.email = new_email
        user.save()

        # messages.success(request, "Tenant updated successfully.")
        return redirect('adminapp:dashboard')

    return render(request, 'adminApp/edit_tenent.html', {'tenant': tenant})


# Delete Owner View
def delete_owner(request, owner_id):
    owner = get_object_or_404(OwnerUser, id=owner_id)

    # Delete the related auth_user entry
    user = User.objects.get(id=owner.user.id)
    user.delete()

    # Delete the OwnerUser entry
    owner.delete()

    return redirect('adminapp:dashboard')


# Delete Tenant View
def delete_tenant(request, tenant_id):
    tenant = get_object_or_404(TenentUser, id=tenant_id)

    # Delete the related auth_user entry
    user = User.objects.get(id=tenant.user.id)
    user.delete()

    # Delete the TenantUser entry
    tenant.delete()

    return redirect('adminapp:dashboard')
