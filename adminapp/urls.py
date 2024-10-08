from django.urls import path, include
from . import views

app_name='adminapp'

urlpatterns = [
    path('homepage/',views.hompage,name='homepage'),

    path('login_or_register/', views.login_or_register, name='login_or_register'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('homepage1/', views.homepage1, name='homepage1'),

]