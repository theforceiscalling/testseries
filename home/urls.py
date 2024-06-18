from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    # path('counter', views.counter, name='counter'),
    # path('registerstudent', views.registerstudent, name='registerstudent'),
    # path('login', views.login, name='login'),
    # path('logout', views.logout, name='logout')
]