from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
@login_required
def index(request):
    if request.user.is_teacher or request.user.is_superuser or request.user.is_staff:
        messages.info(request, "Welcome to teacher account. Here, you can create test papers for your students and make that test as online and offline.")
    else:
        messages.warning(request, "You do not have a verified teacher account. If you want to access this page you can request to convert your Student account into Teacher account (subjectted to approval for authenticity).")
    
    return render(request, 'teacher/index.html')