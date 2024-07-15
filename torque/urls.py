# urls.py
from django.urls import path
from . import views

app_name = 'torque'

urlpatterns = [
    path('upload-pdf', views.upload_pdf, name='upload-pdf'),
]