from django.urls import path
from . import views

app_name='tenentapp'

urlpatterns = [

    path('',views.tenenthompage,name='tenenthomepage'),

]