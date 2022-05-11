from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="predictor"),
    path('predictions/', views.predictions, name="predictions")

]