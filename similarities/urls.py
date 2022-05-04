from django.urls import path
from . import views

urlpatterns = [
    path('similarities', views.index , name='similarities')    
]