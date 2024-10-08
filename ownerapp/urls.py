from django.urls import path
from . import views

app_name='ownerapp'

urlpatterns = [

path('ownerhomepage/',views.ownerhompage,name='ownerhomepage'),

    path('login_or_register1/', views.login_or_register1, name='login_or_register1'),
    path('ohomepage1/', views.ohomepage1, name='ohomepage1'),
    path('upload_property/', views.upload_property, name='upload_property'),
    path('property_list/', views.property_list, name='property_list'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('owner_profile/', views.owner_profile, name='owner_profile'),
]
