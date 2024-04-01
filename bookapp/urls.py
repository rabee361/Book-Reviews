from django.urls import path
from .views import email_temp

urlpatterns = [
    path('email/' ,email_temp)
]