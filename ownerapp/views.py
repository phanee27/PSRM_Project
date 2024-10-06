from django.shortcuts import render

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
                messages.success(request, 'Registration successful! Please log in.')
                return redirect('ownerapp:login_or_register1')
        elif 'login' in request.POST:
            # Login Logic
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

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
                messages.error(request, 'Invalid username or password')

    return render(request, 'ownerApp/loginpage1.html')


@login_required
def ohomepage1(request):
    return render(request, 'ownerApp/ownerHomePage.html', {'username': request.user.username})


from django.shortcuts import render, redirect
from .forms import PropertyForm
from .models import Property

def upload_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ownerapp:property_list')  # Redirect to the list of properties
    else:
        form = PropertyForm()
    return render(request, 'ownerApp/upload_property.html', {'form': form})

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'ownerApp/property_list.html', {'properties': properties})

def property_detail(request, pk):
    property = Property.objects.get(pk=pk)
    return render(request, 'ownerApp/property_detail.html', {'property': property})
