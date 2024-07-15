from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.index, name='accounts_index'),
    path('registerstudent', views.registerstudent, name='registerstudent'),
    path('registerteacher', views.registerteacher, name='registerteacher'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('myaccount', views.myaccount, name='myaccount'),
    path('verify', views.verify, name='verify'),
    path('add-question', views.addquestion, name='neetug_add_question'),
    path('add-question-to-test', views.addquestion_to_test, name='add_question_to_test'),
    path('unauthorized/', views.unauthorized_access, name='unauthorized'),  
    path('account-convert-request/', views.account_convert_request, name='account-convert-request'),
]