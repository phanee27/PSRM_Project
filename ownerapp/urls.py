from django.urls import path
from . import views

app_name='ownerapp'

urlpatterns = [

path('ownerhomepage/',views.ownerhompage,name='ownerhomepage'),

    path('login_or_register1/', views.login_or_register1, name='login_or_register1'),
    path('ohomepage1/', views.ohomepage1, name='ohomepage1'),
]