from django.urls import path
from . import views

app_name='tenentapp'

urlpatterns = [

    path('',views.tenenthompage,name='tenenthomepage'),
    path('tenent_profile/',views.tenent_profile,name='tenent_profile'),
    path('about_us/',views.about_us,name='about_us'),
    path('property_list/',views.property_list,name='property_list'),
    path('property_detail/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/contact/', views.contact_owner, name='contact_owner'),

]