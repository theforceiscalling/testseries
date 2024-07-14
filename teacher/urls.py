from django.urls import path
from teacher import views


urlpatterns = [
    path('', views.index, name='teacher_index'),
]