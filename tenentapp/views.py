from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

def tenenthompage(request):
    return render(request,'tenentApp/tenentHomePage.html')

