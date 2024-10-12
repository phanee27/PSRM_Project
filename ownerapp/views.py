from django.shortcuts import render, get_object_or_404


# Create your views here.
def ownerhompage(request):
    return render(request,'ownerApp/ownerHomePage.html')


from django.shortcuts import render

# Create your views here.

def ohomepage(request):
    return render(request, 'ownerApp/ownerHomepage.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import OwnerUser

# Registration and Login View
def login_or_register1(request):
    if request.method == 'POST':
        if 'register' in request.POST:
            # Registration Logic
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Registration successful! Please complete your profile.')
                # return redirect('ownerapp:owner_profile')  # Redirect to profile creation page
                return redirect('adminapp:login_or_register')  # Redirect to the same page for login
        
        elif 'login' in request.POST:
            # Login Logic
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Create OwnerProfile if not exists
                OwnerProfile.objects.get_or_create(user=user)  # Ensure profile is created

                # Save login data in OwnerUser table if not already present
                if not OwnerUser.objects.filter(user=user).exists():
                    OwnerUser.objects.create(
                        user=user,
                        username=user.username,
                        email=user.email,
                        password=user.password  # Store the hashed password
                    )

                if username == 'admin':
                    return redirect('adminapp:homepage1')
                else:
                    return redirect('ownerapp:ohomepage1')
            else:
                # If authentication fails, check if the username exists
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Incorrect password. Please try again.')
                else:
                    messages.error(request, 'Username not found. Please check your username.')
    return render(request, 'ownerApp/loginpage1.html')


@login_required
def ohomepage1(request):
    return render(request, 'ownerApp/ownerHomePage.html', {'username': request.user.username})


# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def upload_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user  # Set owner to the logged-in user
            property.save()
            return redirect('ownerapp:property_list')
    else:
        form = PropertyForm()
    return render(request, 'ownerApp/upload_property.html', {'form': form})



from ownerapp.models import OwnerUser

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import Property  # Ensure to import the Property model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Property, OwnerUser # Adjust imports if necessary
@login_required
def property_list(request):
    search_query = request.GET.get('search', '')
    filter_option = request.GET.get('filter', '')

    # Initialize variables
    user_type = None
    properties = Property.objects.none()  # Start with an empty queryset

    # Identify the logged-in user type (owner or admin)
    if request.user.username == 'admin' and authenticate(username='admin', password='admin'):
        user_type = 'admin'
        properties = Property.objects.all()  # Admin sees all properties

    # Check if user is an owner
    elif OwnerUser.objects.filter(user=request.user).exists():
        user_type = 'owner'
        properties = Property.objects.filter(owner=request.user)  # Only show properties uploaded by the owner

    # Apply search filter (if any)
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply sorting based on filter option
    if filter_option:
        if filter_option == 'price_asc':
            properties = properties.order_by('price')  # Price low to high
        elif filter_option == 'price_desc':
            properties = properties.order_by('-price')  # Price high to low

    context = {
        'properties': properties,
        'user_type': user_type,  # Pass the user type to the template for navbar logic
    }

    return render(request, 'ownerApp/property_list.html', context)



def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, 'ownerApp/property_detail.html', {'property': property})

# views.py
# views.py
from django.http import HttpResponseForbidden


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .models import Property
from .forms import PropertyForm
@login_required
def edit_property(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')  # Success message
            return redirect('ownerapp:property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'ownerApp/edit_property.html', {'form': form})



@login_required
def delete_property(request, pk):
    property = get_object_or_404(Property, id=pk)

    if property.owner != request.user:  # Ensure only the owner can delete
        return HttpResponseForbidden("You are not allowed to delete this property.")

    if request.method == "POST":
        property.delete()
        return redirect('ownerapp:property_list')

    return render(request, 'confirm_delete.html', {'property': property})


# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OwnerProfile
from .forms import OwnerProfileForm, PropertyForm

# views.py
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import OwnerProfile
from .forms import OwnerProfileForm

@login_required
def owner_profile(request):
    # Ensure there is always an OwnerProfile for the user
    profile, created = OwnerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the profile update form
        form = OwnerProfileForm(request.POST, request.FILES, instance=profile)
        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('ownerapp:owner_profile')  # Redirect to avoid resubmission

        # Handle the password change form
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Password changed successfully!')
                return redirect('ownerapp:owner_profile')  # Redirect to avoid resubmission

    else:
        form = OwnerProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'ownerApp/ownerProfile.html', {
        'form': form,
        'password_form': password_form,
        'profile': profile
    })

def about_us(request):
    return render(request,'ownerApp/about_us.html')