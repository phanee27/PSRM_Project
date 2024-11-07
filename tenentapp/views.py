from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ownerapp.models import OwnerUser ,Property


# Create your views here.

def tenenthompage(request):
    return render(request,'tenentApp/tenentHomePage.html')

def about_us(request):
    return render(request,'tenentApp/about_us.html')

# tenentapp/views.py

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import TenentProfile
from .forms import TenentProfileForm

@login_required
def tenent_profile(request):
    # Ensure there is always a TenentProfile for the user
    profile, created = TenentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Handle the profile update form
        form = TenentProfileForm(request.POST, request.FILES, instance=profile)
        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('tenentapp:tenent_profile')  # Redirect to avoid resubmission

        # Handle the password change form
        password_form = PasswordChangeForm(request.user, request.POST)
        if 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Password changed successfully!')
                return redirect('tenentapp:tenent_profile')  # Redirect to avoid resubmission

    else:
        form = TenentProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)

    return render(request, 'tenentApp/tenentProfile.html', {
        'form': form,
        'password_form': password_form,
        'profile': profile
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q


@login_required
def property_list(request):
    # Check for reset parameter to clear filters
    if 'reset' in request.GET:
        return redirect('tenentapp:property_list')  # Redirect to clear search and filter queries

    search_query = request.GET.get('search', '')
    filter_option = request.GET.get('filter', '')

    # Fetch all properties
    properties = Property.objects.all()

    # Apply search filter (if any)
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(location__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Apply sorting based on filter option
    if filter_option == 'price_asc':
        properties = properties.order_by('price')  # Price low to high
    elif filter_option == 'price_desc':
        properties = properties.order_by('-price')  # Price high to low

    # Determine user type for rendering the correct navbar
    user_type = 'admin' if request.user.is_superuser else 'owner' if OwnerUser.objects.filter(user=request.user).exists() else 'tenant'

    context = {
        'properties': properties,
        'user_type': user_type,
        'search_query': search_query,
        'filter_option': filter_option,
    }

    return render(request, 'tenentApp/property_list.html', context)


@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'tenentApp/property_detail.html', {'property': property})
