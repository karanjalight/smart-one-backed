from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import viewsets
from .viewsets import *
from django.contrib.auth import views as auth_views 

from .views import LoginView, MeterDataView, ValveControlView

urlpatterns = [
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/meter-data/', MeterDataView.as_view(), name='meter-data'),
    path('api/valve-control/', ValveControlView.as_view(), name='valve-control'),
]
